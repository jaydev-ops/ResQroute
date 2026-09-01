import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, KeepTogether, HRFlowable, PageBreak
)
from reportlab.pdfgen import canvas

PDF_FILENAME = "resQroute_Technical_Architecture_and_Implementation_Guide.pdf"

class NumberedCanvas(canvas.Canvas):
    """Canvas for adding page numbers and running headers/footers."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        if self._pageNumber == 1:
            return  # Suppress headers/footers on cover page
        
        self.saveState()
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#64748B"))
        
        # Header
        self.drawString(54, 750, "resQroute — Technical Architecture & Implementation Blueprint")
        self.drawRightString(612 - 54, 750, "SIH Problem Statement SIH26191")
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.5)
        self.line(54, 742, 612 - 54, 742)
        
        # Footer
        self.line(54, 50, 612 - 54, 50)
        self.setFont("Helvetica", 8)
        self.drawString(54, 38, "CONFIDENTIAL — SMART INDIA HACKATHON 2026")
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(612 - 54, 38, page_str)
        self.restoreState()

def build_pdf():
    print(f"Compiling {PDF_FILENAME}...")
    doc = SimpleDocTemplate(
        PDF_FILENAME,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Custom Color Palette
    PRIMARY = colors.HexColor("#0F172A")    # Deep Slate
    SECONDARY = colors.HexColor("#1E293B")  # Card Blue
    ACCENT_BLUE = colors.HexColor("#0284C7")# Sky Blue
    ACCENT_GREEN = colors.HexColor("#059669")# Emerald
    ACCENT_RED = colors.HexColor("#DC2626")  # Crimson
    TEXT_DARK = colors.HexColor("#1E293B")  # Charcoal
    TEXT_MUTED = colors.HexColor("#475569") # Slate

    # Typography Styles
    title_style = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=26,
        leading=32,
        textColor=PRIMARY,
        alignment=0,
        spaceAfter=10
    )

    subtitle_style = ParagraphStyle(
        'CoverSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=ACCENT_BLUE,
        alignment=0,
        spaceAfter=25
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=16,
        leading=20,
        textColor=PRIMARY,
        spaceBefore=18,
        spaceAfter=8,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=ACCENT_BLUE,
        spaceBefore=12,
        spaceAfter=6,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=TEXT_DARK,
        spaceAfter=8
    )

    callout_style = ParagraphStyle(
        'Callout_Text',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=9,
        leading=13,
        textColor=PRIMARY
    )

    code_style = ParagraphStyle(
        'Code_Custom',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=8,
        leading=11,
        textColor=colors.HexColor("#0F172A"),
        spaceAfter=6
    )

    story = []

    # ---------------------------------------------------------
    # COVER / HEADER BLOCK
    # ---------------------------------------------------------
    story.append(Paragraph("resQroute", title_style))
    story.append(Paragraph("Intelligent Hazard-Based Red Zone Identification, Carrying Capacity Assessment & Relocation Platform", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=2, color=ACCENT_BLUE, spaceBefore=0, spaceAfter=15))

    # Meta Table
    meta_data = [
        [Paragraph("<b>SIH Problem Statement:</b> SIH26191", body_style), Paragraph("<b>Target Stack:</b> React + FastAPI + PostGIS", body_style)],
        [Paragraph("<b>Lead Architecture Baseline:</b> Modular Monolith", body_style), Paragraph("<b>Core Thesis:</b> Shortest Route ≠ Safest Route", body_style)],
        [Paragraph("<b>Primary Deliverable:</b> Web-First MVP Platform", body_style), Paragraph("<b>Document Date:</b> August 2026", body_style)]
    ]
    meta_table = Table(meta_data, colWidths=[250, 254])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F8FAFC")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#E2E8F0")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 15))

    # ---------------------------------------------------------
    # SECTION 1: EXECUTIVE SUMMARY & THESIS
    # ---------------------------------------------------------
    story.append(Paragraph("1. Executive Summary & Core Engineering Thesis", h1_style))
    story.append(Paragraph(
        "During natural disasters (floods, landslides, storm surges), the existence of an emergency shelter does not guarantee that vulnerable citizens can safely reach or use it. "
        "Conventional routing systems (Google Maps, Waze) optimize aggressively for shortest distance or travel time, often directing citizens directly into submerged low-lying roads or active hazard zones.",
        body_style
    ))
    
    # Callout Box
    callout_data = [[Paragraph("<b>CORE ARCHITECTURAL PRINCIPLE:</b><br/>"
                               "1. <b>SHORTEST ROUTE ≠ SAFEST ROUTE</b>.<br/>"
                               "2. <b>AI ASSISTS — VALIDATED DATA, SAFETY CONSTRAINTS & DETERMINISTIC ROUTING DECIDE</b>.<br/>"
                               "3. <b>SMS PROVIDES A FALLBACK COMMUNICATION CHANNEL — resQroute PROVIDES THE INTELLIGENCE</b>.", callout_style)]]
    callout_table = Table(callout_data, colWidths=[504])
    callout_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F0FDF4")),
        ('BOX', (0,0), (-1,-1), 1.5, ACCENT_GREEN),
        ('PADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(callout_table)
    story.append(Spacer(1, 15))

    # ---------------------------------------------------------
    # SECTION 2: SYSTEM OVERVIEW DIAGRAM & STACK
    # ---------------------------------------------------------
    story.append(Paragraph("2. System Architecture & Component Scope", h1_style))
    if os.path.exists("diagrams/diagram_01_system_overview.png"):
        story.append(Image("diagrams/diagram_01_system_overview.png", width=480, height=280))
        story.append(Paragraph("<i>Figure 1: High-Level Modular Monolith System Architecture</i>", ParagraphStyle('Cap', parent=body_style, fontName='Helvetica-Oblique', fontSize=8, alignment=1)))
        story.append(Spacer(1, 10))

    scope_data = [
        ["Component", "Classification", "Technical Scope & Technology Stack"],
        ["Responsive Web Map", "[MVP]", "React 18 + TypeScript + Leaflet / MapLibre + Tailwind CSS"],
        ["API Gateway", "[MVP]", "Python FastAPI + Pydantic + Redis Pub/Sub WebSockets"],
        ["Overlay Routing Engine", "[MVP]", "OSRM Candidates + PostGIS ST_Intersects Dynamic Edge Filter"],
        ["Shelter Capacity", "[MVP]", "Append-Only shelter_updates Event Stream + Materialized View"],
        ["Simulated SMS Gateway", "[MVP]", "Compact text response parser modal for web demonstration"],
        ["Shadow ML Classifier", "[ENHANCED]", "NLP text report classification & image debris checking in shadow mode"],
        ["BLE Mesh SOS", "[ADVANCED]", "Peer-to-peer experimental device mesh for zero-connectivity signals"]
    ]
    scope_table = Table(scope_data, colWidths=[120, 84, 300])
    scope_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 8.5),
        ('BOTTOMPADDING', (0,0), (-1,0), 6),
        ('BACKGROUND', (0,1), (-1,-1), colors.HexColor("#F8FAFC")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('FONTSIZE', (0,1), (-1,-1), 8),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(scope_table)
    story.append(Spacer(1, 15))

    # ---------------------------------------------------------
    # SECTION 3: DETERMINISTIC ROUTING & POSTGIS OVERLAYS
    # ---------------------------------------------------------
    story.append(Paragraph("3. Routing Decision Engine & PostGIS Dynamic Overlays", h1_style))
    story.append(Paragraph(
        "To avoid misleading terminology: OSRM's preprocessed road graph is static and does not serve as a live dynamic-risk engine by itself. "
        "Instead, `resQroute` uses OSRM to generate K-shortest candidate paths, after which PostGIS performs dynamic spatial overlay checks (`ST_Intersects`) against active closed edge buffers (`road_edge_overlays`).",
        body_style
    ))
    
    if os.path.exists("diagrams/diagram_04_routing_decision_overlay.png"):
        story.append(Image("diagrams/diagram_04_routing_decision_overlay.png", width=480, height=280))
        story.append(Paragraph("<i>Figure 2: PostGIS Overlay Routing Decision Pipeline</i>", ParagraphStyle('Cap', parent=body_style, fontName='Helvetica-Oblique', fontSize=8, alignment=1)))
        story.append(Spacer(1, 10))

    # ---------------------------------------------------------
    # SECTION 4: POSTGIS DATA ARCHITECTURE & ERD
    # ---------------------------------------------------------
    story.append(Paragraph("4. PostGIS Data Architecture & Audit Schemas", h1_style))
    story.append(Paragraph(
        "All hazard reports, road edge closures, and shelter occupancy changes maintain strict data lineage. "
        "The data model incorporates audit tables (`road_edge_overlays`, `hazard_evidence`, `source_registry`, `audit_events`, `shelter_updates`) to ensure every published hazard identifies its source, freshness, and actor history.",
        body_style
    ))
    
    if os.path.exists("diagrams/diagram_11_postgis_er_diagram.png"):
        story.append(Image("diagrams/diagram_11_postgis_er_diagram.png", width=480, height=280))
        story.append(Paragraph("<i>Figure 3: PostgreSQL + PostGIS Safety & Audit ER Diagram</i>", ParagraphStyle('Cap', parent=body_style, fontName='Helvetica-Oblique', fontSize=8, alignment=1)))
        story.append(Spacer(1, 10))

    # ---------------------------------------------------------
    # SECTION 5: SAFETY ASSERTIONS & TEST SUITES
    # ---------------------------------------------------------
    story.append(Paragraph("5. Behavioral Safety Assertions & Test Suites", h1_style))
    
    test_data = [
        ["Suite ID", "Disaster Condition", "Behavioral Safety Assertion"],
        ["TS-001", "Road Edge #402 Closed", "Confirmed closed edges MUST NEVER appear in returned evacuation routes."],
        ["TS-002", "Shelter Occupancy = 100%", "Full shelters MUST NEVER be recommended; auto-redirect to next nearest."],
        ["TS-003", "Wheelchair Profile Active", "Routes with stairs/steep slopes MUST BE REJECTED; ramp mandatory."],
        ["TS-004", "Data Sync > 30m Stale", "System MUST trigger explicit stale warning banner or return NO_SAFE_ROUTE."],
        ["TS-005", "Unverified Citizen Report", "Raw report CANNOT create hard closure without policy evidence or authority action."]
    ]
    test_table = Table(test_data, colWidths=[55, 120, 329])
    test_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), ACCENT_BLUE),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 8.5),
        ('BACKGROUND', (0,1), (-1,-1), colors.HexColor("#F8FAFC")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('FONTSIZE', (0,1), (-1,-1), 8),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(test_table)
    story.append(Spacer(1, 15))

    # ---------------------------------------------------------
    # SECTION 6: BEGINNER GLOSSARY (35 TERMS)
    # ---------------------------------------------------------
    story.append(Paragraph("6. Beginner Technical Glossary", h1_style))
    
    glossary_items = [
        ("API", "Application Programming Interface allowing frontend and backend services to exchange structured data."),
        ("Backend", "Server-side logic and database operations processing user requests asynchronously."),
        ("Frontend", "User interface layer running in web browsers built with HTML, CSS, and JavaScript/TypeScript."),
        ("GIS", "Geographic Information System designed to capture, store, analyze, and manage spatial data."),
        ("GPS", "Global Positioning System providing location coordinates (latitude and longitude) via satellite."),
        ("PostgreSQL", "Open-source object-relational database management system offering high reliability and SQL compliance."),
        ("PostGIS", "Spatial database extension for PostgreSQL adding support for geographic objects and spatial queries."),
        ("Redis", "In-memory data structure store used for sub-millisecond caching and real-time WebSocket pub/sub messaging."),
        ("REST", "Representational State Transfer architectural style for stateless, HTTP-based web services."),
        ("WebSocket", "Full-duplex, persistent communication protocol enabling instant server-to-client broadcasts."),
        ("ML", "Machine Learning algorithms that detect patterns and make predictions from historical data."),
        ("LLM", "Large Language Model trained on extensive text datasets for natural language processing and extraction."),
        ("NLP", "Natural Language Processing algorithms analyzing unstructured text into structured hazard records."),
        ("Computer Vision", "AI models processing digital images to identify structural damage, flooding, or debris."),
        ("Routing Engine", "Software algorithm calculating navigable paths between geographic points on a network graph."),
        ("Graph", "Mathematical data structure comprising vertices (nodes) connected by edges (roads)."),
        ("Node", "A point in a network graph representing an intersection or geographic landmark."),
        ("Edge", "A line segment in a network graph representing a physical road segment connecting two nodes."),
        ("GeoJSON", "Standard open format for encoding geographic data structures using JSON objects."),
        ("Docker", "Containerization platform packaging software code and dependencies into portable containers."),
        ("Cloud", "On-demand availability of remote computer system resources and storage over the internet."),
        ("Cache", "High-speed data storage layer storing transient data for rapid retrieval without database hits."),
        ("RBAC", "Role-Based Access Control restricting system features based on authorized user roles."),
        ("JWT", "JSON Web Token securely transmitting verified user identity claims between client and server."),
        ("BLE", "Bluetooth Low Energy wireless protocol for short-range low-power device communication."),
        ("MQTT", "Lightweight messaging protocol tailored for resource-constrained Internet of Things (IoT) sensors."),
        ("IoT", "Network of physical devices embedded with sensors to exchange real-time environmental data."),
        ("ETL", "Extract, Transform, Load data pipeline processing raw inputs into structured analytical tables."),
        ("Inference", "Execution phase of a trained machine learning model generating predictions on new input data."),
        ("Training", "Process of optimizing machine learning model weights on labeled historical datasets."),
        ("Validation", "Evaluating machine learning model accuracy on unbiased dataset splits to prevent overfitting."),
        ("Precision", "Proportion of true positive predictions among all positive predictions made by a model."),
        ("Recall", "Proportion of true positive predictions identified out of all actual positive cases in dataset."),
        ("F1 Score", "Harmonic mean of precision and recall measuring overall classification accuracy."),
        ("Deterministic Routing", "Routing logic producing identical, predictable outputs for a given set of spatial constraints.")
    ]

    glossary_table_data = [["Term", "Definition"]]
    for term, definition in glossary_items:
        glossary_table_data.append([Paragraph(f"<b>{term}</b>", body_style), Paragraph(definition, body_style)])

    glossary_table = Table(glossary_table_data, colWidths=[120, 384])
    glossary_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 8.5),
        ('BACKGROUND', (0,1), (-1,-1), colors.HexColor("#F8FAFC")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('PADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(glossary_table)
    story.append(Spacer(1, 15))

    # ---------------------------------------------------------
    # SECTION 7: PHASED ROADMAP & FINAL PRINCIPLE
    # ---------------------------------------------------------
    story.append(Paragraph("7. Phased Implementation Roadmap", h1_style))
    if os.path.exists("diagrams/diagram_12_mvp_phased_roadmap.png"):
        story.append(Image("diagrams/diagram_12_mvp_phased_roadmap.png", width=480, height=240))
        story.append(Paragraph("<i>Figure 4: Phased Development Engineering Roadmap</i>", ParagraphStyle('Cap', parent=body_style, fontName='Helvetica-Oblique', fontSize=8, alignment=1)))
        story.append(Spacer(1, 10))

    story.append(Paragraph(
        "<b>FINAL IMPLEMENTATION PHILOSOPHY:</b><br/>"
        "<i>\"Build the reliable core first. Add intelligence second. Add resilience third. Scale only after validation.\"</i><br/><br/>"
        "resQroute does not simply find the nearest shelter. It evaluates whether the shelter is suitable, reachable, and safe for the person who needs it.",
        callout_style
    ))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully compiled {PDF_FILENAME}!")

if __name__ == "__main__":
    build_pdf()
