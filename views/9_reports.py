import streamlit as st
import pandas as pd
import numpy as np
import io
from datetime import datetime, timedelta

st.set_page_config(page_title="Reports Center", page_icon="📑", layout="wide")
st.title("📑 Reports Center & Automated Exports")
st.caption("Generate, customize, export, and schedule business intelligence reports.")

# Helper to load report data
@st.cache_data(ttl=3600)
def generate_report_data(report_type, start_date, end_date):
    np.random.seed(42)
    date_range = pd.date_range(start=start_date, end=end_date, freq="D")
    if len(date_range) == 0:
        date_range = pd.date_range(end=datetime.now(), periods=10, freq="D")

    if report_type == "Sales Summary Report":
        df = pd.DataFrame({
            "Date": np.random.choice(date_range, size=150),
            "Order_ID": [f"ORD-{10000+i}" for i in range(150)],
            "Category": np.random.choice(["Electronics", "Clothing", "Home & Kitchen", "Books"], size=150),
            "Payment_Mode": np.random.choice(["UPI", "Credit Card", "Net Banking", "COD"], size=150),
            "Sales_Amount": np.random.uniform(500, 25000, size=150).round(2),
            "Tax_Amount": np.random.uniform(50, 2500, size=150).round(2),
            "Status": np.random.choice(["Completed", "Completed", "Completed", "Refunded"], size=150)
        })
    elif report_type == "Customer Activity Report":
        df = pd.DataFrame({
            "Customer_ID": [f"CUST-{2000+i}" for i in range(100)],
            "Customer_Name": [f"User {i+1}" for i in range(100)],
            "Total_Orders": np.random.randint(1, 30, size=100),
            "Total_Spent": np.random.uniform(1000, 200000, size=100).round(2),
            "Last_Active": np.random.choice(date_range, size=100),
            "Segment": np.random.choice(["VIP", "Loyal", "Regular", "At-Risk"], size=100)
        })
    elif report_type == "Inventory Stock Report":
        df = pd.DataFrame({
            "SKU": [f"SKU-{3000+i}" for i in range(80)],
            "Product_Name": [f"Item {i+1}" for i in range(80)],
            "Category": np.random.choice(["Electronics", "Clothing", "Home & Kitchen"], size=80),
            "Current_Stock": np.random.randint(0, 500, size=80),
            "Reorder_Level": np.random.randint(20, 50, size=80),
            "Unit_Price": np.random.uniform(100, 5000, size=80).round(2),
            "Stock_Status": np.random.choice(["In Stock", "Low Stock", "Out of Stock"], size=80)
        })
    else:  # Employee Performance Report
        df = pd.DataFrame({
            "Emp_ID": [f"EMP-{100+i}" for i in range(40)],
            "Employee_Name": [f"Employee {i+1}" for i in range(40)],
            "Department": np.random.choice(["Sales", "Support", "Logistics", "Marketing"], size=40),
            "Tasks_Completed": np.random.randint(50, 300, size=40),
            "Performance_Rating": np.random.choice(["A+", "A", "B", "C"], size=40),
            "Revenue_Generated": np.random.uniform(50000, 500000, size=40).round(2)
        })
    return df

# Helper to generate basic PDF bytes using ReportLab (with fallback)
def generate_pdf_report(df, title):
    try:
        from reportlab.lib.pagesizes import letter, landscape
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib import colors

        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=landscape(letter), rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)
        elements = []

        styles = getSampleStyleSheet()
        title_style = ParagraphStyle('TitleStyle', parent=styles['Heading1'], fontSize=18, textColor=colors.HexColor('#1E3A8A'))
        
        elements.append(Paragraph(f"<b>{title}</b>", title_style))
        elements.append(Paragraph(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))
        elements.append(Spacer(1, 15))

        # Convert Top 25 rows for PDF table
        pdf_df = df.head(25)
        table_data = [list(pdf_df.columns)] + pdf_df.astype(str).values.tolist()

        t = Table(table_data)
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1E3A8A')),
            ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('FONTSIZE', (0,0), (-1,0), 9),
            ('BOTTOMPADDING', (0,0), (-1,0), 6),
            ('BACKGROUND', (0,1), (-1,-1), colors.HexColor('#F3F4F6')),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#D1D5DB')),
            ('FONTSIZE', (0,1), (-1,-1), 8),
        ]))
        
        elements.append(t)
        doc.build(elements)
        buffer.seek(0)
        return buffer.getvalue()
    except Exception:
        # Fallback to text string formatted as bytes if ReportLab fails
        output = f"--- {title} ---\nGenerated: {datetime.now()}\n\n" + df.head(25).to_string()
        return output.encode('utf-8')

# Sidebar Filters
st.sidebar.header("🎯 Report Controls")
report_type = st.sidebar.selectbox(
    "Select Report Type",
    ["Sales Summary Report", "Customer Activity Report", "Inventory Stock Report", "Employee Performance Report"]
)

d_col1, d_col2 = st.sidebar.columns(2)
start_date = d_col1.date_input("Start Date", datetime.now() - timedelta(days=30))
end_date = d_col2.date_input("End Date", datetime.now())

df_report = generate_report_data(report_type, start_date, end_date)

# Main Navigation Tabs
tab1, tab2, tab3 = st.tabs(["📊 Live Preview & Export", "🖨️ Print View", "⏰ Scheduled Reports"])

# TAB 1: Live Preview & Export
with tab1:
    st.subheader(f"📑 {report_type}")
    
    # Key Summary Metrics
    m1, m2, m3 = st.columns(3)
    m1.metric("Total Records", f"{len(df_report):,}")
    
    if "Sales_Amount" in df_report.columns:
        m2.metric("Total Revenue", f"₹{df_report['Sales_Amount'].sum():,.2f}")
        m3.metric("Avg Order Value", f"₹{df_report['Sales_Amount'].mean():,.2f}")
    elif "Total_Spent" in df_report.columns:
        m2.metric("Total Customer Spend", f"₹{df_report['Total_Spent'].sum():,.2f}")
        m3.metric("Avg Spend / Customer", f"₹{df_report['Total_Spent'].mean():,.2f}")
    elif "Current_Stock" in df_report.columns:
        m2.metric("Total Units in Stock", f"{df_report['Current_Stock'].sum():,}")
        m3.metric("Low Stock Items", f"{len(df_report[df_report['Stock_Status'] == 'Low Stock']):,}")
    else:
        m2.metric("Total Tasks Completed", f"{df_report['Tasks_Completed'].sum():,}")
        m3.metric("Total Revenue Generated", f"₹{df_report['Revenue_Generated'].sum():,.2f}")

    st.markdown("---")
    
    # Download Action Buttons
    col_dl1, col_dl2, _ = st.columns([1, 1, 2])
    
    # CSV Download Button
    csv_bytes = df_report.to_csv(index=False).encode('utf-8')
    col_dl1.download_button(
        label="📥 Download CSV",
        data=csv_bytes,
        file_name=f"{report_type.lower().replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv",
        use_container_width=True
    )
    
    # PDF Download Button
    pdf_bytes = generate_pdf_report(df_report, report_type)
    col_dl2.download_button(
        label="📄 Download PDF",
        data=pdf_bytes,
        file_name=f"{report_type.lower().replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.pdf",
        mime="application/pdf",
        use_container_width=True
    )

    st.markdown("### Data Table")
    st.dataframe(df_report, use_container_width=True, hide_index=True)

# TAB 2: Print View
with tab2:
    st.subheader("🖨️ Printer-Friendly Preview")
    st.caption("Press Ctrl+P (or Cmd+P) in your browser to print this formatted report directly.")

    print_html = f"""
    <style>
        @media print {{
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            .no-print {{ display: none; }}
            table {{ width: 100%; border-collapse: collapse; margin-top: 15px; }}
            th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; font-size: 12px; }}
            th {{ background-color: #1E3A8A; color: white; }}
        }}
        .report-header {{ border-bottom: 2px solid #1E3A8A; padding-bottom: 10px; margin-bottom: 15px; }}
    </style>
    <div class="report-header">
        <h2 style="color: #1E3A8A; margin: 0;">{report_type}</h2>
        <p style="margin: 5px 0; color: #555;">Date Range: {start_date} to {end_date} | Generated On: {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
    </div>
    """
    st.markdown(print_html, unsafe_allow_html=True)
    st.dataframe(df_report.head(50), use_container_width=True, hide_index=True)

# TAB 3: Scheduled Reports
with tab3:
    st.subheader("⏰ Automated Report Scheduling")
    st.write("Configure recurring email reports to be delivered directly to stakeholders.")

    # Schedule Form
    with st.form("schedule_report_form"):
        s_col1, s_col2 = st.columns(2)
        target_report = s_col1.selectbox("Report to Schedule", ["Sales Summary", "Customer Activity", "Inventory Stock", "Employee Performance"])
        frequency = s_col2.selectbox("Frequency", ["Daily (08:00 AM)", "Weekly (Monday)", "Monthly (1st Day)"])

        e_col1, e_col2 = st.columns(2)
        recipient_email = e_col1.text_input("Recipient Email Address", placeholder="manager@company.com")
        export_format = e_col2.selectbox("Attachment Format", ["PDF", "CSV", "Both (PDF & CSV)"])

        is_active = st.checkbox("Enable Schedule Immediately", value=True)
        submit_schedule = st.form_submit_button("🚀 Save Schedule Config")

    if submit_schedule:
        if not recipient_email:
            st.error("Please enter a valid recipient email address.")
        else:
            st.success(f"✅ Schedule saved successfully! '{target_report}' will be sent {frequency} to {recipient_email}.")

    st.markdown("---")
    st.subheader("📋 Active Scheduled Jobs")
    
    # Mock Schedule Table
    schedules_df = pd.DataFrame([
        {"Job ID": "SCH-101", "Report": "Sales Summary", "Frequency": "Daily (08:00 AM)", "Recipient": "ceo@company.com", "Format": "PDF", "Status": "Active"},
        {"Job ID": "SCH-102", "Report": "Inventory Stock", "Frequency": "Weekly (Monday)", "Recipient": "warehouse@company.com", "Format": "CSV", "Status": "Active"},
        {"Job ID": "SCH-103", "Report": "Customer Activity", "Frequency": "Monthly (1st Day)", "Recipient": "marketing@company.com", "Format": "Both", "Status": "Paused"}
    ])
    st.dataframe(schedules_df, use_container_width=True, hide_index=True)