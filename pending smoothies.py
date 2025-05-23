
# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col, when_matched
from snowflake.snowpark import Session  # Make sure this import is at the top
cnx = st.connection("snowflake")
session = cnx.session()
#Session._set_active_session(session)


# Write directly to the app
st.title(":cup_with_straw: Pending Smoothie Orders  :cup_with_straw:")
st.write ("""Orders that need to filled.""")

#option = st.selectbox('What is your favourite fruit?',
 #                    ('Banana','Strawberries','Peaches'))


#session = get_active_session()
# my_dataframe = session.table("smoothies.public.orders").filter(col("ORDER_FILLED")==0).collect()
snow_df = session.table("smoothies.public.orders").filter(col("ORDER_FILLED") == 0)
my_dataframe = snow_df.to_pandas()

if not my_dataframe.empty:
        
        st.dataframe(data=my_dataframe, use_container_width=True)
        editable_df = st.data_editor(my_dataframe)
        
        #submitted = st.button('Submit')
        
        if st.button('Submit'):
          
        
            og_dataset = session.table("smoothies.public.orders")
            edited_dataset = session.create_dataframe(editable_df)
            try:
               og_dataset.merge(edited_dataset
                             , (og_dataset['ORDER_UID'] == edited_dataset['ORDER_UID'])
                             , [when_matched().update({'ORDER_FILLED': edited_dataset['ORDER_FILLED']})]
                            )
               st.success ("Order(s) updated!",icon = '👍')
            except:
                st.write ('Something want wrong.')
else:
 st.success ("There are no pending orders right now",icon = '👍')
