import pandas as pd
from thefuzz import fuzz

def fuzzy_compare_rows(
        subject:pd.Series,
        reference:pd.Series,
        fuzzy_weights:dict["col","weight"],
        exact_weights:dict["col","weight"]
    ):
    """
    Compares columns on a pair of rows to determine how similar they are.
    To achieve this, it compares uses the specified columns
        * either by using fuzzy search (on the columns specified by the keys of `fuzzy_weights`)
        * or exact match (on the columns specified by the keys of `exact_weights`)
    The values of the weights dictionaries must be numbers, representing the relative importance of that comparison.
    """
    total = sum(fuzzy_weights.values()) + sum(exact_weights.values())
    fuzzy_terms = [fuzz.partial_ratio(subject[col],reference[col])/100*weight for col,weight in fuzzy_weights.items()]
    exact_terms = [(subject[col]==reference[col])*weight for col,weight in exact_weights.items()]
    return sum(fuzzy_terms+exact_terms)/total

def fuzzy_canonicalize(
        queries:pd.DataFrame,
        canonical:pd.DataFrame,
        fuzzy_weights:dict["col","weight"],
        exact_weights:dict["col","weigth"]={},
        report_found_values=True,
        progress=False
    ):
    """
    Given the `queries` dataframe, whose rows are possibly mispelled strings identifiers,
    and the `canonical` dataframe, wich you are sure are the correct identifiers,
    this functions searches each query row into the canonical dataframe,
    and returns a dataframe with the index of the most similar canon row.

    This search is done via the `fuzzy_compare_rows` function, and as such,
    you specify the fuzzy and exact matches colums via two dictionaries,
    along with their weights.

    With the `report_found_values` you can control if the canon founded values
    are shown in the result.
    """
    if progress:
        from tqdm import tqdm
        tqdm.pandas()
        scores = queries.progress_apply(
            lambda x: canonical.apply(
                fuzzy_compare_rows,
                axis=1,
                reference=x,
                fuzzy_weights=fuzzy_weights,
                exact_weights=exact_weights
            ),
            axis=1,
        )
    else:
        scores = queries.apply(
            lambda x: canonical.apply(
                fuzzy_compare_rows,
                axis=1,
                reference=x,
                fuzzy_weights=fuzzy_weights,
                exact_weights=exact_weights
            ),
            axis=1,
        )
    results = pd.concat([
            scores.max(axis=1).rename("match_score"),
            scores.idxmax(axis=1).rename("canon_index")
    ],axis=1)
    if report_found_values:
        report_columns = sorted(list(set(fuzzy_weights.keys()) | set(exact_weights.keys())))
        report = pd.concat([canonical.loc[results.canon_index,col] for col in report_columns],axis=1)
        report.index = results.index
        results = pd.concat([results,report],axis=1)
    return results.sort_values("match_score",ascending=False)

def fuzzy_scoped_canonicalize(
        queries:pd.DataFrame,
        canonical:pd.DataFrame,
        on_column:str,
        scoping:dict["value","index list"],
        fuzzy_weights:dict["col","weight"],
        exact_weights:dict["col","weigth"]={},
        report_found_values=True,
        progress=False
    ):
    """
    Same as `fuzzy_canonicalize` but grouping the queries by the `on_column`.
    On each iteration, each value of the `on_column` is used to filter the `canonical` DataFrame,
    accoding to the `scoping` dict.
    This is useful if the comparison function is slow, if `canonical` is itself too large,
    or if you want to limit the search by some criterion (like geographical proximity).

    The returned DataFrame has identical format to that of the `fuzzy_canonicalize` function.

    The values of the `scoping` dict should be indexes of `canonical`.
    """
    group_results = []
    if progress:
        from tqdm import tqdm
        for pivot,group in tqdm(queries.groupby(on_column)):
            filtered_canon = canonical.loc[scoping[pivot]]
            group_results.append(
                fuzzy_canonicalize(group,filtered_canon,fuzzy_weights,exact_weights,report_found_values)
            )
    else:
        for pivot,group in queries.groupby(on_column):
            filtered_canon = canonical.loc[scoping[pivot]]
            group_results.append(
                fuzzy_canonicalize(group,filtered_canon,fuzzy_weights,exact_weights,report_found_values)
            )
    return pd.concat(group_results).sort_index().sort_values("match_score",ascending=False)
