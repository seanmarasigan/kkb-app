import streamlit as st
import pandas as pd
from crud_utils import delete_member, edit_member, add_member, clear_text
from order_utils import order

# Initialize session state variables
if 'kkb_group' not in st.session_state:
    st.session_state.kkb_group = {}

if 'kkb_member_input' not in st.session_state:
    st.session_state.kkb_member_input = ""

if 'editing' not in st.session_state:
    st.session_state.editing = False

if 'edit_key' not in st.session_state:
    st.session_state.edit_key = ""

if 'new_name' not in st.session_state:
    st.session_state.new_name = ""

if 'order_lst' not in st.session_state:
    st.session_state.order_lst = {
        "item": [],
        "price": [],
        "quantity": [],
        "kkb_members": []
    }



def main():

    st.title("KKB")

    with st.sidebar:
        st.title("KKB Group")

        # Display current members from session state with edit/delete buttons
        if len(st.session_state.kkb_group):
            for key, member in st.session_state.kkb_group.items():
                col1, col2, col3 = st.columns([3, 1, 1])
                with col1:
                    st.write(member)
                with col2:
                    if st.button(f":pencil2:", key=f"edit-{member}"):
                        st.session_state.edit_key = key
                        st.session_state.new_name = member #prefill with current name
                        st.session_state.editing = True
                        st.rerun()

                with col3:
                    if st.button(":wastebasket:", key=f"del-{member}"):
                        delete_member(st.session_state, key)
        else:
            st.write("No KKB members yet.")

        # Conditional rendering for the edit form
        if st.session_state.editing:
            #now is safe to render the input, it won't generate error
            st.session_state.new_name = st.text_input("Enter new name:", value=st.session_state.new_name, key='edit_name_input')
            col1, col2, col3 = st.columns([3, 1, 1])
            with col2:
                if st.button(f"💾"):
                    edit_member(st.session_state, st.session_state.edit_key, st.session_state.new_name)
                    st.session_state.editing = False  # Reset editing flag after saving
                    st.rerun()
            with col3:
                if st.button("❌"):
                    st.session_state.editing = False  # Reset editing flag on cancel
                    st.rerun()
        else:
        #only render this input when user is not editing
            kkb_member = st.text_input("Enter name:",  key='kkb_member_input')
            if st.button("Add member", on_click=lambda: add_member(st.session_state, kkb_member)):
                st.rerun()

    if st.button("Add order"):
        order(st.session_state, st.session_state.kkb_group)

    if len(st.session_state.order_lst["item"]) and len(st.session_state.kkb_group):
        st.subheader("Current Bill: ")
        df = pd.DataFrame(st.session_state.order_lst)

    
        col1, col2, col3 = st.columns([3, 1, 1])
        with col1:
            st.write("Item")
            for i in range(len(st.session_state.order_lst["item"])):
                st.markdown(
                    f"<p>{st.session_state.order_lst["item"][i]}</p>",
                    unsafe_allow_html=True
                )
        
            st.write("Total")

        with col2:
            st.markdown(
                f"<p style='text-align: right'>Quantity</p>",
                unsafe_allow_html=True
            )
            for i in range(len(st.session_state.order_lst["item"])):
                st.markdown(
                    f"<p style='text-align: right'>{st.session_state.order_lst["quantity"][i]}</p>",
                    unsafe_allow_html=True
                )
        
        with col3:
            st.markdown(
                f"<p style='text-align: right'>Amount</p>",
                unsafe_allow_html=True
            )
            for i in range(len(st.session_state.order_lst["item"])):
                st.markdown(
                    f"<p style='text-align: right'>₱{st.session_state.order_lst["price"][i]:,.2f}</p>",
                    unsafe_allow_html=True
                )
            
            st.session_state.order_lst["quantity"] = pd.to_numeric(st.session_state.order_lst["quantity"])
            st.session_state.order_lst["price"] = pd.to_numeric(st.session_state.order_lst["price"])
            st.session_state.order_lst["Total"] = st.session_state.order_lst["quantity"] * st.session_state.order_lst["price"]
            st.markdown(
                f"<p style='text-align: right'>₱{st.session_state.order_lst["Total"].sum():,.2f}</p>",
                unsafe_allow_html=True
            )

        with st.expander("Breakdown"):


            payments = {}

            for _, row in df.iterrows():
                total_price = row["price"] * row["quantity"]
                members = row["kkb_members"]
                share = total_price / len(members)  # Divide cost among members
                
                for member in members:
                    if member in payments:
                        payments[member]["amount"] += share
                        payments[member]["items"].append(row["item"])
                    else:
                        payments[member] = {"amount": share, "items": [row["item"]]}

            # Convert payments dictionary to DataFrame
            payments_df = pd.DataFrame([
                {"Member": member, "Amount to Pay": amount["amount"], "Paid Items": ", ".join(amount["items"])}
                    for member, amount in payments.items()
                ])
            payments_df['Amount to Pay'] = payments_df['Amount to Pay'].apply(lambda x: f'₱{x:,.2f}')

            # Reorder columns
            payments_df = payments_df[['Member','Paid Items', 'Amount to Pay']]

            st.dataframe(payments_df, use_container_width=True)

    else:
        st.write("There are no orders yet or no KKB members.")


if __name__ == "__main__":
    main()


