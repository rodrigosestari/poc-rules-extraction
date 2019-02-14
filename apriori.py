import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules
from sklearn.preprocessing import OneHotEncoder


def get_rules(transactions):
    transactions = transactions[["account_id",
                                 "booking_type",
                                 "business",
                                 "categorylevel_id",
                                 "description",
                                 "recipient_iban",
                                 "sender_iban"]]
    transactions.fillna("<UNK>", inplace=True)
    ohe = OneHotEncoder(sparse=False, dtype=bool).fit(transactions)
    frequent_itemsets = apriori(pd.DataFrame(ohe.transform(transactions), columns=ohe.get_feature_names()),
                                min_support=0.1,
                                use_colnames=True)

    rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=0.7)
    print("**ALL RULES** \n")
    print(rules[["antecedents", "consequents"]].to_string(index=False))

    categories_rules = pd.concat(list(map(lambda x: rules[rules['consequents'] == {x}],
                                          list(filter(lambda x: str(x).startswith('x3_'), ohe.get_feature_names())))))

    print("**CATEGORIES RULES** \n")
    print(categories_rules[["antecedents", "consequents"]].to_string(index=False))


transactions = pd.read_json("data/transactions.gzip", orient='records', lines=True, compression='gzip')

get_rules(transactions[transactions["business"] == 760])
get_rules(transactions)
get_rules(transactions[transactions["business"] == 837])
