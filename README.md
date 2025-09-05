INVENTORY MANAGEMENT OF URBAN RETAIL Co.
# 📊 Streamlit Dashboard for Inventory Insights

An interactive **data-driven dashboard** built with **Streamlit**, connected to a **PostgreSQL backend (Supabase)**.  
This project helps **URBAN Retail Co.** (demo case) improve inventory management by providing real-time insights, alerts, and recommendations.

🔗 **Live App:** [Streamlit App](https://appdashboard1-mzwqkzj34ktns6gfs6vyir.streamlit.app/)  
💻 **GitHub Repo:** [Streamlit_dashboard1](https://github.com/achla1407/Streamlit_dashboard1)

---

## 🚀 Project Overview

The dashboard enables smarter stock management by:

- Displaying **real-time inventory metrics**  
- Highlighting **low-stock items**  
- Recommending **restocking actions** based on demand trends  

## 🧩 Schema & Data Flow

The database schema is designed using an **ER diagram** to model:

- `Products`  
- `Store`  
- `Time`  
- `Region`  

Data is accessed via **SQLAlchemy** with Supabase’s connection pooling.  
SQL queries use **joins and aggregations** to ensure performance and scalability.

---

## ⚙️ Recommendation Logic

The system uses a **threshold-based heuristic**:

- 🔴 **Urgent Reorder** → `inventory_level == 0` (Stockout)  
- 🟠 **Reorder Soon** → Inventory below forecasted demand  
- 🟢 **Stock OK** → Healthy inventory aligned with demand  
- 🔵 **Reduce Holding** → Inventory > 2× expected demand (Overstock)  

✅ Why this works:
- Prevents stockouts by **flagging low inventory early**  
- Avoids overstocking by **reducing holding costs**  
- Simple, explainable, and adjustable for business needs  


## 📊 Key Insights Delivered

1. **Low Stock Alerts** → Early warnings to avoid stockouts  
2. **Top-Selling Items** → Ranked list of best-selling products  
3. **Inventory Turnover Trends** → FAST vs SLOW movers  
4. **Category-Level Analysis** → Spot trends across product groups  

## ✅ Recommendations

- Automate restocking → integrate with procurement system  
- Use **dynamic thresholds** → seasonal/moving averages  
- Enable **report exports** → CSV/PDF for sharing insights  


## 🛠️ Tech Stack

- **Frontend:** Streamlit  
- **Backend:** PostgreSQL (Supabase)  
- **Deployment:** Streamlit Cloud  
- **ORM/Data Access:** SQLAlchemy with connection pooling  



