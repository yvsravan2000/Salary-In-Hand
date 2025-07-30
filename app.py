# Import packages and modules | External
import streamlit as st

# Page configuration
with st.spinner(text="Loading...", show_time=True):
    # Configure the page
    st.set_page_config(
        page_title="SalaryInHand",
        page_icon=":material/currency_rupee_circle:",
        layout="centered",
        initial_sidebar_state="auto",
        menu_items={
            "Get Help": f"mailto:yvsravan2000@gmail.com"
        }
    )

############################### Page functions ###############################
def indian_number_format(amount: float) -> str:
    """
    Formats a given number in the Indian number system (e.g., 12,34,56,789.00).

    Args:
        amount (float): The numerical value to format.

    Returns:
        str: Formatted string representing the number in Indian format with 2 decimal places.
             Negative numbers are preserved (e.g., -12,34,567.89).

    Function Description:
        This function takes a floating-point number and converts it into a string formatted
        according to the Indian number system, which uses commas after every two digits beyond
        the first three digits from the right. It maintains up to two decimal places.
    """
    # Check if the amount is negative
    is_negative = amount < 0

    # Use the absolute value and round to two decimal places
    amount = abs(round(amount, 2))

    # Split into integer and decimal parts as strings
    integer_part, _, decimal_part = f"{amount:.2f}".partition('.')

    # Format the integer part using Indian style commas
    n = len(integer_part)
    if n <= 3:
        # If 3 or fewer digits, no additional commas needed
        formatted = integer_part
    else:
        # Start with the rightmost 3 digits
        formatted = integer_part[-3:]
        integer_part = integer_part[:-3]
        # Add commas after every 2 digits in the remaining part
        while len(integer_part) > 0:
            formatted = integer_part[-2:] + ',' + formatted
            integer_part = integer_part[:-2]

    # Combine integer and decimal parts
    result = f"{formatted}.{decimal_part}"

    # Prefix minus sign if original amount was negative
    return f"-{result}" if is_negative else result


def calculate_tax(taxable_amount: float) -> float:
    """
    Calculate the total income tax based on progressive Indian tax brackets.

    Args:
        taxable_amount (float): The taxable income for which tax needs to be calculated.

    Returns:
        float: The total tax computed according to the specified progressive tax slabs.

    Function Description:
        Given a taxable amount, the function computes income tax using predefined
        slab rates as per Indian standards. For every bracket amount exceeded, the tax
        is calculated at the bracket rate and summed cumulatively.
    """
    # List of (income limit, tax rate) tuples, ordered from highest to lowest bracket
    brackets = [
        (2400000, 0.30),  # 30% for income above 24,00,000
        (2000000, 0.25),  # 25% for income above 20,00,000
        (1600000, 0.20),  # 20% for income above 16,00,000
        (1200000, 0.15),  # 15% for income above 12,00,000
        (800000,  0.10),  # 10% for income above 8,00,000
        (400000,  0.05),  # 5% for income above 4,00,000
    ]

    tax_value = 0.0

    # For each bracket, if there is surplus income above the limit,
    # apply the bracket's rate and reduce the amount for further calculation
    for limit, rate in brackets:
        if taxable_amount > limit:
            tax_value += (taxable_amount - limit) * rate
            taxable_amount = limit  # Only lower bracket rates apply on remaining amount

    return tax_value

############################### Page contents ###############################
# Title
st.title(":primary-background[ :primary[:material/currency_rupee_circle:] Salary:primary[In]Hand]")
st.divider()

with st.form(key="inhand_salary_input_form", clear_on_submit=False, enter_to_submit=True, border=True, width="stretch"):
    # Input cols
    col1, col2 = st.columns(2)

    # Input for salary
    inp_fixed_salary = float(col1.number_input(
        label="Fixed Gross Salary (in INR)",
        min_value=0.0,
        value=1800000.0,
        step=1000.0,
        format="%.2f",
        placeholder="12345567.89",
        help="Enter your gross salary to calculate the tax amount."
    ))

    # Input for Employer NPS contribution
    inp_nps = float(col2.number_input(
        label="Employer NPS Contribution (% of basic salary)",
        min_value=0.0,
        max_value=14.0,
        value=14.0,
        step=1.0,
        format="%.2f",
        placeholder="14.00",
        help="Enter the employer's NPS contribution to calculate the in-hand salary."
    ))

    # Input for tax regime
    inp_tax_regime = st.selectbox(
        label="Select Tax Regime",
        options=["Old Tax Regime", "New Tax Regime"],
        index=1,  # Default to New Tax Regime
        help="Choose the tax regime to calculate the in-hand salary.",
        disabled=True  # Currently disabled as the tax calculation is based on the new tax regime
    )

    submit_button_clicked = st.form_submit_button(
        label="Calculate In-Hand Salary",
        type="primary",
        use_container_width=True,
        help="Click to calculate your in-hand salary based on the provided inputs."
    )

if(submit_button_clicked):
    with st.spinner(text="Calculating...", show_time=True):
        # Calculate the variable pay (assuming 14% of fixed gross salary)
        variable_pay = inp_fixed_salary * 0.14

        # Calculate the ctc (Cost to Company)
        ctc_amount = inp_fixed_salary + variable_pay

        # Calculate the basic salary (assuming 40% of fixed gross salary)
        basic_salary = inp_fixed_salary * 0.40

        # Calculate the employer's NPS contribution
        employer_nps_contribution = (inp_nps / 100) * basic_salary

        # Calculate the employer's PF contribution
        employer_pf_contribution = 0.12 * basic_salary

        # Calculate the employee PF contribution
        employee_pf_contribution = 0.12 * basic_salary

        # Calculate the gratuity contribution (assuming 4.8% of basic salary)
        gratuity_contribution = 0.048 * basic_salary

        # Calculate the professional tax (assuming a flat rate of 300 per month)
        professional_tax = 300 * 12

        # Calculate the taxable amount
        taxable_amount = inp_fixed_salary - employer_nps_contribution - employer_pf_contribution - gratuity_contribution - 75000

        # Calculate the tax amount
        tax_amount = calculate_tax(taxable_amount)

        # Calculate the CESS amount
        cess_amount = 0.04 * tax_amount

        # Calculate the in-hand salary
        in_hand_salary = inp_fixed_salary - employer_nps_contribution - employer_pf_contribution - gratuity_contribution - employee_pf_contribution - professional_tax - tax_amount - cess_amount
        
        # Display results
        st.toast(body="In-hand salary calculated successfully!", icon=":material/check_circle:")
        with st.expander("Calculations", expanded=False):
            st.markdown(
                """
                | Component | Amount (₹) |
                |-----------|------------|
                | CTC Amount | {} |
                | :red[*]Variable Pay (14% of Fixed Salary) | {} |
                | Basic Salary (40% of Fixed Salary) | {} |
                | Employer NPS Contribution | {} |
                | Employer PF Contribution (12% of Basic Salary) | {} |
                | Employee PF Contribution (12% of Basic Salary) | {} |
                | Gratuity Contribution (4.8% of Basic Salary) | {} |
                | Professional Tax (Flat Rate) | {} |
                """.format(
                    indian_number_format(ctc_amount),
                    indian_number_format(variable_pay),
                    indian_number_format(basic_salary),
                    indian_number_format(employer_nps_contribution),
                    indian_number_format(employer_pf_contribution),
                    indian_number_format(employee_pf_contribution),
                    indian_number_format(gratuity_contribution),
                    indian_number_format(professional_tax)
                )
            )
            st.markdown(":red[*]_Not considered in taxable income._")

        with st.expander("In-Hand Salary", expanded=True):
            st.markdown(
                """
                | Component | Amount/Year (₹) | Amount/Month (₹) |
                |-----------|------------------|------------------|
                | CTC | {} | {} |
                | Gross Salary | {} | {} |
                | Taxable Amount | {} | {} |
                | Income Tax Amount | {} | {} |
                | Health & Education CESS Amount | {} | {} |
                | PF & Pension | {} | {} |
                | **Net Salary** | **{}** | **:green-background[:green[{}]]** |
                """.format(
                    indian_number_format(ctc_amount),
                    indian_number_format(ctc_amount / 12),
                    indian_number_format(inp_fixed_salary),
                    indian_number_format(inp_fixed_salary / 12),
                    indian_number_format(taxable_amount),
                    indian_number_format(taxable_amount / 12),
                    indian_number_format(tax_amount),
                    indian_number_format(tax_amount / 12),
                    indian_number_format(cess_amount),
                    indian_number_format(cess_amount / 12),
                    indian_number_format(employer_nps_contribution + employer_pf_contribution + employee_pf_contribution),
                    indian_number_format((employer_nps_contribution + employer_pf_contribution + employee_pf_contribution) / 12),
                    indian_number_format(in_hand_salary),
                    indian_number_format(in_hand_salary / 12)
                )
            )
