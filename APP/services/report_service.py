"""
report_service.py
====================
Generates a downloadable PDF report for a completed interview analysis
using ReportLab, styled with the application's lavender / pink / green
theme accents. Also provides a helper to load structured report data for
the HTML report view.
"""

import os
import json
import logging

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable,
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

from APP.database import db, Report, Analysis, Interview, User

logger = logging.getLogger("ai_interview_analyzer.report_service")

THEME_LAVENDER = colors.HexColor("#8E6FB0")
THEME_PINK = colors.HexColor("#F7C6D9")
THEME_GREEN = colors.HexColor("#3FA66E")
THEME_TEXT = colors.HexColor("#3A2E4D")


def get_report_bundle(interview_id: int) -> dict:
    """Load Report + Analysis + Interview + User rows and parse JSON fields for template use."""
    report = Report.query.filter_by(interview_id=interview_id).first()
    analysis = Analysis.query.filter_by(interview_id=interview_id).first()
    interview = db.session.get(Interview, interview_id)
    user = db.session.get(User, interview.user_id) if interview else None

    return {
        "report": report,
        "analysis": analysis,
        "interview": interview,
        "user": user,
        "strengths": json.loads(report.strengths_json) if report and report.strengths_json else [],
        "weaknesses": json.loads(report.weaknesses_json) if report and report.weaknesses_json else [],
        "tips": json.loads(report.tips_json) if report and report.tips_json else [],
    }


def generate_pdf_report(interview_id: int, output_dir: str) -> str:
    """
    Build a polished PDF report for the given interview and return the
    absolute path of the generated file.
    """
    bundle = get_report_bundle(interview_id)
    interview, analysis, user, report = (
        bundle["interview"], bundle["analysis"], bundle["user"], bundle["report"],
    )
    if not interview or not analysis:
        raise ValueError(f"No completed analysis found for interview {interview_id}")

    os.makedirs(output_dir, exist_ok=True)
    pdf_path = os.path.join(output_dir, f"report_interview_{interview_id}.pdf")

    doc = SimpleDocTemplate(pdf_path, pagesize=A4,
                             topMargin=20 * mm, bottomMargin=18 * mm,
                             leftMargin=18 * mm, rightMargin=18 * mm)
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle("TitleLavender", parent=styles["Title"], textColor=THEME_LAVENDER, fontSize=22)
    heading_style = ParagraphStyle("HeadingGreen", parent=styles["Heading2"], textColor=THEME_GREEN, spaceBefore=14)
    body_style = ParagraphStyle("BodyText2", parent=styles["BodyText"], textColor=THEME_TEXT, leading=16)

    elements = []
    elements.append(Paragraph("AI Interview Analyzer — Performance Report", title_style))
    elements.append(Spacer(1, 4 * mm))
    elements.append(HRFlowable(width="100%", thickness=1.2, color=THEME_PINK))
    elements.append(Spacer(1, 6 * mm))

    candidate_name = user.full_name if user else "Candidate"
    elements.append(Paragraph(f"<b>Candidate:</b> {candidate_name}", body_style))
    elements.append(Paragraph(f"<b>Interview:</b> {interview.title}", body_style))
    elements.append(Paragraph(f"<b>Overall Score:</b> {analysis.overall_score} / 100 ({analysis.verdict})", body_style))
    elements.append(Spacer(1, 6 * mm))

    elements.append(Paragraph("Dimension Scores", heading_style))
    score_data = [["Dimension", "Score"]] + [
        [dim.title(), f"{score:.1f}"] for dim, score in analysis.dimension_scores().items()
    ]
    table = Table(score_data, colWidths=[100 * mm, 40 * mm])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), THEME_LAVENDER),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, THEME_PINK]),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#E0D3EE")),
        ("TEXTCOLOR", (0, 1), (-1, -1), THEME_TEXT),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    elements.append(table)
    elements.append(Spacer(1, 6 * mm))

    elements.append(Paragraph("Feedback Summary", heading_style))
    elements.append(Paragraph(report.feedback_text or "No feedback available.", body_style))
    elements.append(Spacer(1, 4 * mm))

    if bundle["strengths"]:
        elements.append(Paragraph("Strengths", heading_style))
        for s in bundle["strengths"]:
            elements.append(Paragraph(f"• {s.get('description', '')}", body_style))

    if bundle["weaknesses"]:
        elements.append(Paragraph("Areas to Improve", heading_style))
        for w in bundle["weaknesses"]:
            elements.append(Paragraph(f"• {w.get('description', '')}", body_style))

    if bundle["tips"]:
        elements.append(Paragraph("Improvement Tips", heading_style))
        for tip_group in bundle["tips"]:
            elements.append(Paragraph(f"<b>{tip_group.get('dimension', '').title()}</b>", body_style))
            for tip in tip_group.get("tips", []):
                elements.append(Paragraph(f"• {tip}", body_style))

    doc.build(elements)

    report.pdf_path = pdf_path
    from APP.database import db
    db.session.commit()

    logger.info("Generated PDF report for interview %s at %s", interview_id, pdf_path)
    return pdf_path
