# Import python packages
import streamlit as st
# from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col, when_matched

# Write directly to the app
st.title(":timer_clock: Pending Smoothie Orders :timer_clock:")
st.write(
  """Orders that need to be filled
  """)

# session = get_active_session()
cnx = st.connection("snowflake")
session = cnx.session()
# my_dataframe = session.table("smoothies.public.orders") \
my_dataframe = session.sql('select * from smoothies.public.orders order by 1') \
    .filter(col("ORDER_FILLED") == 0) \
    .collect()
# st.dataframe(data=my_dataframe, use_container_width=True)

if my_dataframe:
    editable_df = st.data_editor(my_dataframe)
    submitted = st.button('Submit')

    if submitted:
        # st.success('Order completed',icon="🎉")
        # st.write("Order Filled", submitted.ORDER_UID)
        # I want to show who's order is filled 
        og_dataset = session.table("smoothies.public.orders")
        edited_dataset = session.create_dataframe(editable_df)

        try:
            og_dataset.merge(edited_dataset
                     , (og_dataset['ORDER_UID'] == edited_dataset['ORDER_UID'])
                     , [when_matched().update({'ORDER_FILLED': edited_dataset['ORDER_FILLED']})]
                    )
            st.success("Order(s) Updated!",icon="🎉")
        except:
            st.write('Something went wrong.')
else:
    st.success('There are no pending orders right now', icon="👍")


