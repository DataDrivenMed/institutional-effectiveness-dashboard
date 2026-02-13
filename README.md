# Enterprise Institutional Effectiveness Dashboard

A dean-level decision-support dashboard for academic medical center leadership. Consolidates education outcomes, research enterprise, workforce analytics, and accreditation compliance into a single executive view.

## Live Demo

[View the live dashboard →](https://institutional-effectiveness-dashboard.streamlit.app)

## What It Does

This dashboard answers four strategic questions:

| Domain | Decision Question |
|--------|-------------------|
| **Education** | Are students succeeding, and where do we need to intervene? |
| **Research** | Is research funding growing, and are we diversifying revenue? |
| **Workforce** | Are we building a diverse, stable, and productive faculty? |
| **Compliance** | Are we ready for the next LCME visit, and where are the gaps? |

Every chart includes a narrative caption explaining **what it means** for leadership.

## Design Philosophy

- **Board-packet quality**: Minimal colors, high whitespace, big numbers
- **Decision-oriented**: Every visualization answers a specific leadership question
- **No jargon**: Accessible to non-technical senior leaders
- **Screenshot-ready**: Each tab stands alone as a PDF for presentations

## Tech Stack

- **Streamlit** — Interactive web application
- **Plotly** — Clean, professional charts
- **Pandas / NumPy** — Data generation and transformation

## Data

This is a **demonstration** using synthetic data modeled on realistic academic medical center metrics. No institutional data is included.

## Local Development

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Author

**Per Nilsson**  
Director, Accreditation & Strategic Planning  
[LinkedIn](https://linkedin.com/in/pernilsson) · [GitHub](https://github.com/pernilsson)

---

*Built as part of a decision-architecture portfolio demonstrating enterprise analytics for academic medicine leadership.*
