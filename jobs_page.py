import streamlit as st
import pandas as pd

def jobs_page(job_requirements):
    st.header('Job Requirements')
    search_term = st.text_input("Search by jd_details:")

    # Filter data based on the search term
    filtered_df_search = job_requirements[
        (job_requirements['jd_details'].str.contains(search_term, case=False, na=False)) 
    ]
    with st.expander("Job Requirements"):
        st.dataframe(filtered_df_search, hide_index=True, use_container_width=True)
    
    
    # Radio buttons for selecting action
    action = st.radio(
        "Choose an Action:",
        options=["Edit Job Details", "Add New Job", "Remove Job"],
    )

    if action == "Edit Job Details":
        st.subheader("Edit Job Details")

        # Dropdown menu to select a job with a placeholder option
        job_ids = job_requirements["job_id"].tolist()
        job_ids.insert(0, "Select a Job ID")  # Add a placeholder option

        selected_job_id = st.selectbox("Select Job ID:", job_ids)

        if selected_job_id and selected_job_id != "Select a Job ID":
            # Retrieve current details
            current_row = job_requirements[
                job_requirements["job_id"] == selected_job_id
            ].iloc[0]

            updated_job_details = st.text_input("Job Details:", value=current_row.get("jd_details", ""))
            updated_jd_location = st.text_input("Job Location:", value=current_row.get("job_location", ""))
            updated_bill_rate = st.text_input("Job Bill Rate:", value=current_row.get("bill_rate", ""))
            updated_visas = st.text_input("Visas:", value=current_row.get("visas", ""))
            updated_Description = st.text_input("Description:", value=current_row.get("Description", ""))
            updated_Client = st.text_input("Client:", value=current_row.get("Client", ""))

            if st.button("Save Changes", key="edit_save_changes"):
                # Update the details in the dataframe
                job_requirements.loc[
                    job_requirements["job_id"] == selected_job_id,
                    [
                        "jd_details",
                        "job_location",
                        "bill_rate",
                        "visas",
                        "Description",
                        "Client",
                    ],
                ] = (
                    updated_job_details,
                    updated_jd_location,
                    updated_bill_rate,
                    updated_visas,
                    updated_Description,
                    updated_Client,
                )

                # Save the updated job details back to the CSV file
                job_requirements.to_csv(
                    "D:/Einsteinium Labs/Projects/ATS/ATS_V1/data/job_requirements.csv",
                    index=False,
                )

                st.success(f"Details updated for Job ID {selected_job_id}!")
                st.session_state.updated = True

    # ---------------- ADD NEW JOB ----------------
    elif action == "Add New Job":
        st.subheader("Add New Job")

        # Form to add a new job
        with st.form("add_job_form"):
            new_jd_details = st.text_input("Job Details:", value="")
            new_jd_location = st.text_input("Job Location:", value="")
            new_job_bill_rate = st.text_input("Job Bill Rate:", value="")
            new_visas = st.text_input("Visas:", value="")
            new_Description = st.text_input("Description:", value="")
            new_Client = st.text_input("Client:", value="")

            submitted = st.form_submit_button("Submit")
            if submitted:
                new_row = {
                    "job_id": job_requirements["job_id"].max() + 1 if not job_requirements.empty else 1,
                    "jd_details": new_jd_details,
                    "job_location": new_jd_location,
                    "bill_rate": new_job_bill_rate,
                    "visas": new_visas,
                    "Description": new_Description,
                    "Client": new_Client,
                }

                # Update the dataframe
                job_requirements = pd.concat(
                    [job_requirements, pd.DataFrame([new_row])], ignore_index=True
                )

                # Save the updated job details back to the CSV file
                job_requirements.to_csv(
                    "D:/Einsteinium Labs/Projects/ATS/ATS_V1/data/job_requirements.csv",
                    index=False,
                )

                st.success("New job added successfully!")
                st.session_state.updated = True

    # ---------------- REMOVE JOB ----------------
    elif action == "Remove Job":
        st.subheader("Remove Job")

        # Dropdown menu to select a job with a placeholder option
        job_ids = job_requirements["job_id"].tolist()
        job_ids.insert(0, "Select a Job ID")  # Add a placeholder option

        selected_job_id = st.selectbox("Select Job ID to Remove:", job_ids)

        if selected_job_id and selected_job_id != "Select a Job ID":
            if st.button("Remove Job"):
                # Remove the job from the dataframe
                job_requirements = job_requirements[
                    job_requirements["job_id"] != selected_job_id
                ]

                # Save the updated job details back to the CSV file
                job_requirements.to_csv(
                    "D:/Einsteinium Labs/Projects/ATS/ATS_V1/data/job_requirements.csv",
                    index=False,
                )

                st.success(f"Job ID {selected_job_id} removed successfully!")
                st.session_state.updated = True


# Load data from CSV
def load_job_data(filepath):
    try:
        return pd.read_csv(filepath)
    except FileNotFoundError:
        st.warning("File not found. Starting with an empty dataset.")
        return pd.DataFrame(
            columns=[
                "job_id",
                "job_details",
                "job_location",
                "bill_rate",
                "visas",
                "Description",
                "Client"
            ]
        )

# Main execution
def main():
    # Initialize session state for updates if it doesn't exist
    if "updated" not in st.session_state:
        st.session_state.updated = False

    filepath = "D:/Einsteinium Labs/Projects/ATS_V1/data/D:\Einsteinium Labs\Projects\ATS\ATS_V1\data\job_requirements.csv"
    job_detail = load_job_data(filepath)

    # Refresh functionality (optional)
    if st.session_state.updated:
        st.session_state.updated = False
        job_detail = load_job_data(filepath)

    jobs_page(job_detail)


if __name__ == "__main__":
    main()
