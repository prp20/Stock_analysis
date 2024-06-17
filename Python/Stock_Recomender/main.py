import pandas as pd
import utils
import time


def main():
    companies = pd.read_csv('ind_nifty100list.csv')
    funamental_df = pd.read_csv('fund_data.csv')
    # comp_tick_list = companies.Symbol.to_list()
    # funds_list = []
    # for idx, val in enumerate(comp_tick_list):
    #     if idx % 10 == 0 and idx != 0:
    #         time.sleep(15)
    #         print("Sleeping Complete")
    #     value = utils.get_company_fundamentals(val)
    #     funds_list.append(value)
    # funamental_df = pd.DataFrame.from_dict(funds_list)
    res_df = companies.merge(funamental_df, on='Symbol', how='outer')
    utils.insert_df_to_db("stocksdb", "company_basic_data", res_df)


if __name__ == "__main__":
    main()
