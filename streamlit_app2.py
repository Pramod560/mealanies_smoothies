# Import python packages
import streamlit as st
#from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col, when_matched

st.title(":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write(
    f"""Orders that need to be filled
    """
)

# Models & Technologies Information
with st.expander("ℹ️ Models & Technologies Used"):
    st.write("### Data Models")
    st.write("**Database Model:** Snowflake Data Warehouse")
    st.write("- `smoothies.public.orders` - Customer orders with fulfillment tracking")
    st.write("- Order status managed through `order_filled` field")
    
    st.write("### Technology Stack")
    st.write("**Frontend:** Streamlit Web Framework")
    st.write("**Data Processing:** Pandas + Snowflake Snowpark")
    st.write("**Database:** Snowflake Cloud Data Platform")
    st.write("**Order Management:** Real-time order status updates")

#session = get_active_session()
cnx = st.connection('snowflake')
session  = cnx.session()
my_dataframe = session.table("smoothies.public.orders").filter(col('order_filled')==0).collect()

if my_dataframe:
   editable_df = st.data_editor(my_dataframe)
   Submitted = st.button('Submit')

   if Submitted:
        og_dataset = session.table("smoothies.public.orders")
        edited_dataset = session.create_dataframe(editable_df)
        try:
            og_dataset.merge(edited_dataset
                     , (og_dataset['ORDER_UID'] == edited_dataset['ORDER_UID'])
                     , [when_matched().update({'ORDER_FILLED': edited_dataset['ORDER_FILLED']})]
                    )
            st.success('Order(s) Updated!', icon = '👍')
        except:  
            st.success('Something Went Wrong')
else:
    st.success('There are no pending orders!', icon = '👍')
