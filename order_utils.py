import streamlit as st


@st.dialog("Oder details")
def order(session_state, kkb_group):
    
    kkb_members = []
    if len(st.session_state.kkb_group):
        item = st.text_input("Item")
        quantity = st.number_input("Quantity", step=1)
        price = st.number_input("Price", format="%0.2f", step=0.1)
        st.write("Select members:")
        for member in kkb_group:
            i = st.checkbox(member)
            if i:
                kkb_members.append(member)
        

        col1, col2 = st.columns([3, 1])
        with col2:
            if st.button("Add order", key="add-order"):
                session_state.order_lst["item"].append(item)
                session_state.order_lst["quantity"].append(quantity)
                session_state.order_lst["price"].append(price)
                session_state.order_lst["kkb_members"].append(kkb_members)
                print(kkb_members)
                print(session_state.order_lst)
                st.rerun()
                        
                
    else:
        st.write("There are no KKB members yet.")
    


    

    