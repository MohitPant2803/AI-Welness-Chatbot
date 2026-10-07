# server/utils/pdf_generator.py
import json
import os
import tempfile
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.graphics.shapes import Drawing, Rect, String
from reportlab.graphics.charts.piecharts import Pie, LegendedPie
from reportlab.graphics.charts.linecharts import HorizontalLineChart
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.widgets.markers import makeMarker
from reportlab.graphics.charts.legends import Legend

# Reuse all the functions from your paste.txt file
def format_date(date_str):
    """Format date string from ISO to readable format"""
    try:
        date_obj = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        return date_obj.strftime('%b %d, %Y')
    except:
        return date_str

def create_mood_indicator(mood):
    """Create a color code for the mood"""
    mood_colors = {
        'happy': colors.green,
        'tendingToHappy': colors.limegreen,
        'neutral': colors.gold,
        'sad': colors.orange,
        'angry': colors.red,
        'irritated': colors.orangered
    }
    
    return mood_colors.get(mood.lower(), colors.gray)

def create_report(data, output_pdf, company_name="Deloitte", logo_path="", pagesize=A4):
    """
    Create individual employee report PDF from data dictionary
    """
    # Use your existing create_individual_employee_report function but modify it to accept data directly
    # instead of reading from a JSON file
    
    # Create the PDF document
    doc = SimpleDocTemplate(
        output_pdf,
        pagesize=pagesize,
        leftMargin=1.5*cm,
        rightMargin=1.5*cm,
        topMargin=2*cm,
        bottomMargin=2*cm
    )
    
    # Create styles
    styles = getSampleStyleSheet()
    
    # Create custom styles with unique names similar to the general report
    title_style = ParagraphStyle(
        name='CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        alignment=TA_CENTER,
        spaceAfter=10,
        textColor=colors.darkblue
    )
    
    subtitle_style = ParagraphStyle(
        name='CustomSubtitle',
        parent=styles['Heading2'],
        fontSize=18,
        textColor=colors.navy,
        spaceAfter=8
    )
    
    section_header_style = ParagraphStyle(
        name='SectionHeader',
        parent=styles['Heading3'],
        fontSize=16,
        textColor=colors.darkblue,
        spaceBefore=12,
        spaceAfter=8
    )
    
    normal_style = ParagraphStyle(
        name='CustomNormal',
        parent=styles['Normal'],
        fontSize=10,
        spaceBefore=4,
        spaceAfter=4
    )
    
    metric_title_style = ParagraphStyle(
        name='MetricTitle',
        parent=styles['Normal'],
        fontSize=12,
        textColor=colors.darkslategray,
        alignment=TA_CENTER
    )
    
    metric_value_style = ParagraphStyle(
        name='MetricValue',
        parent=styles['Heading2'],
        fontSize=24,
        textColor=colors.darkblue,
        alignment=TA_CENTER,
        spaceAfter=0
    )
    
    alert_style = ParagraphStyle(
        name='AlertStyle',
        parent=styles['Normal'],
        fontSize=11,
        textColor=colors.white,
        backColor=colors.red,
        borderColor=colors.black,
        borderWidth=1,
        borderPadding=5,
        alignment=TA_CENTER,
        spaceBefore=10,
        spaceAfter=10
    )
    
    # Elements to build the PDF
    elements = []
    
    # Add logo if provided
    if logo_path and os.path.exists(logo_path):
        logo = Image(logo_path, width=2*inch, height=1*inch)
        logo.hAlign = 'CENTER'
        elements.append(logo)
        elements.append(Spacer(1, 0.5*cm))
    
    # Get user details
    user_details = data.get('briefUserDetails', {})
    user_name = user_details.get('name', 'Unknown Employee')
    
    # Add title
    elements.append(Paragraph(f"Employee Well-being Report", title_style))
    elements.append(Paragraph(f"{user_name}", subtitle_style))
    
    # Add date with a nicer format
    date_string = datetime.now().strftime("%B %d, %Y")
    date_style = ParagraphStyle(
        name='DateStyle',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.gray,
        alignment=TA_CENTER,
        fontName='Helvetica-Oblique'
    )
    elements.append(Paragraph(f"Generated on: {date_string}", date_style))
    
    # Add decorative line
    elements.append(Spacer(1, 0.3*cm))
    
    # Create a horizontal line
    def add_line(width, color=colors.lightgrey):
        line = Drawing(width, 3)
        line.add(Rect(0, 0, width, 1, fillColor=color, strokeColor=None))
        return line
    
    elements.append(add_line(doc.width))
    elements.append(Spacer(1, 1*cm))
    
    # Check for escalation status
    is_escalated = user_details.get('isEscalated', False)
    if is_escalated:
        # Create a more visually appealing alert box
        alert_text = "⚠️ This employee's case has been escalated and requires attention ⚠️"
        elements.append(Paragraph(alert_text, alert_style))
        elements.append(Spacer(1, 0.7*cm))
    
    # Employee Profile Section
    elements.append(Paragraph("Employee Profile", section_header_style))
    
    # Create profile table
    profile_data = [
        ["Employee ID:", user_details.get('empid', 'N/A')],
        ["Department:", user_details.get('dept', 'N/A')],
        ["Last Active:", format_date(user_details.get('lastActive', 'N/A'))],
        ["Current Mood:", user_details.get('currentMood', 'N/A')],
        ["Work Hours:", f"{user_details.get('workHours', 'N/A')} hours"]
    ]
    
    profile_table = Table(profile_data, colWidths=[doc.width*0.3, doc.width*0.7])
    
    # Get mood color for styling
    mood_color = create_mood_indicator(user_details.get('currentMood', 'neutral'))
    lighter_mood_color = colors.Color(
        min(1.0, mood_color.red + 0.4),
        min(1.0, mood_color.green + 0.4),
        min(1.0, mood_color.blue + 0.4)
    )
    
    # Enhanced styling for profile table - similar to general report
    profile_table.setStyle(TableStyle([
        # Header styling with gradient-like colors
        ('BACKGROUND', (0, 0), (0, 0), colors.lightsteelblue),
        ('BACKGROUND', (0, 1), (0, 1), colors.lightsteelblue),
        ('BACKGROUND', (0, 2), (0, 2), colors.lightsteelblue),
        ('BACKGROUND', (0, 3), (0, 3), colors.lightsteelblue),
        ('BACKGROUND', (0, 4), (0, 4), colors.lightsteelblue),
        
        # Text colors and alignment
        ('TEXTCOLOR', (0, 0), (0, -1), colors.darkblue),
        ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
        ('ALIGN', (1, 0), (1, -1), 'LEFT'),
        
        # Font styling
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        
        # Padding
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (0, -1), 15),
        ('RIGHTPADDING', (0, 0), (0, -1), 15),
        
        # Borders
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('BOX', (0, 0), (-1, -1), 1, colors.darkgrey),
        
        # Highlight mood row with appropriate color
        ('BACKGROUND', (1, 3), (1, 3), lighter_mood_color),
    ]))
    elements.append(profile_table)
    elements.append(Spacer(1, 0.5*cm))
    
    # Add brief mood summary if available
    brief_mood_summary = user_details.get('briefMoodSummary', '')
    if brief_mood_summary:
        elements.append(Paragraph("<b>Mood Summary:</b> " + brief_mood_summary, normal_style))
        elements.append(Spacer(1, 0.5*cm))
    
    # Engagement Metrics
    elements.append(Paragraph("Engagement Metrics", section_header_style))
    
    metrics_data = [
        [
            Paragraph("Team Messages", metric_title_style),
            Paragraph("Emails Sent", metric_title_style),
            Paragraph("Meetings", metric_title_style)
        ],
        [
            Paragraph(f"{user_details.get('teamMessages', 0)}", metric_value_style),
            Paragraph(f"{user_details.get('emailsSent', 0)}", metric_value_style),
            Paragraph(f"{user_details.get('meetings', 0)}", metric_value_style)
        ]
    ]
    
    metrics_table = Table(metrics_data, colWidths=[doc.width/3, doc.width/3, doc.width/3])
    # Enhanced styling for metrics table - matching the general report
    metrics_table.setStyle(TableStyle([
        # Header styling
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightsteelblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.darkslategray),
        
        # Value cell styling with consistent colors from general report
        ('BACKGROUND', (0, 1), (0, 1), colors.lavender),
        ('BACKGROUND', (1, 1), (1, 1), colors.lightcyan),
        ('BACKGROUND', (2, 1), (2, 1), colors.paleturquoise),
        
        # Alignment
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        
        # Padding
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('TOPPADDING', (0, 0), (-1, -1), 12),
        
        # Borders
        ('BOX', (0, 0), (-1, -1), 1, colors.darkgrey),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.lightgrey),
    ]))
    elements.append(metrics_table)
    elements.append(Spacer(1, 1*cm))
    
    # Mood Trends
    mood_trends = data.get('pastFiveMoodTrends', [])
    if mood_trends:
        elements.append(Paragraph("Mood History", section_header_style))
        
        # Create a table for mood history
        mood_headers = ["Date", "Mood"]
        mood_data = [mood_headers]
        
        for mood_entry in mood_trends:
            mood_data.append([
                format_date(mood_entry.get('date', '')),
                mood_entry.get('mood', 'Unknown')
            ])
        
        mood_table = Table(mood_data, colWidths=[doc.width*0.6, doc.width*0.4])
        mood_table.setStyle(TableStyle([
            # Header styling - matching the general report
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightsteelblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.darkslategray),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            
            # Cell styling
            ('ALIGN', (0, 1), (0, -1), 'CENTER'),
            ('ALIGN', (1, 1), (1, -1), 'CENTER'),
            ('FONTNAME', (0, 1), (0, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (0, -1), 10),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
            ('TOPPADDING', (0, 1), (-1, -1), 8),
            
            # Borders and grid - matching the general report
            ('BOX', (0, 0), (-1, -1), 1, colors.darkgrey),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.lightgrey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.Color(0.95, 0.95, 0.95)]),
        ]))
        
        # Add colors to mood cells based on mood
        for i, row in enumerate(mood_data[1:], 1):
            mood = row[1]
            mood_color = create_mood_indicator(mood)
            lighter_mood_color = colors.Color(
                min(1.0, mood_color.red + 0.4),
                min(1.0, mood_color.green + 0.4),
                min(1.0, mood_color.blue + 0.4)
            )
            mood_table.setStyle(TableStyle([
                ('BACKGROUND', (1, i), (1, i), lighter_mood_color),
            ]))
        
        elements.append(mood_table)
        elements.append(Spacer(1, 0.8*cm))
    
    
    # Add a decorative header for the page
    header_style = ParagraphStyle(
        name='PageHeader',
        parent=styles['Heading1'],
        fontSize=22,
        alignment=TA_CENTER,
        spaceAfter=10,
        textColor=colors.darkblue,
        fontName='Helvetica-Bold'
    )
    elements.append(Paragraph("Employee Insights", header_style))
    elements.append(add_line(doc.width, colors.darkblue))
    elements.append(Spacer(1, 0.8*cm))
    
    elements.append(Paragraph("Mood Analysis & Recommendations", section_header_style))
    
    # Add current mood rate if available
    current_mood_rate = data.get('currentMoodRate', '')
    if current_mood_rate:
        elements.append(Paragraph(f"<b>Current Mood Rate:</b> {current_mood_rate}", normal_style))
        elements.append(Spacer(1, 0.3*cm))
    
    # Add mood analysis if available
    mood_analysis = data.get('moodAnalysis', '')
    if mood_analysis:
        elements.append(Paragraph("<b>Analysis:</b>", normal_style))
        # Split the analysis into paragraphs for better readability
        paragraphs = mood_analysis.split('. ')
        for para in paragraphs:
            if para.strip():
                elements.append(Paragraph(para + ".", normal_style))
        elements.append(Spacer(1, 0.5*cm))
    
    # Add recommended action if available
    recommended_action = data.get('recommendedAction', '')
    if recommended_action:
        elements.append(Paragraph("<b>Recommended Action:</b>", normal_style))
        elements.append(Paragraph(recommended_action, normal_style))
        elements.append(Spacer(1, 0.8*cm))
    
    # Achievements & Recognition
    badges = data.get('earnedBadges', [])
    awards = data.get('companyAwards', [])
    
    if badges or awards:
        elements.append(Paragraph("Achievements & Recognition", section_header_style))
        
        # Add badges if available
        if badges:
            elements.append(Paragraph("<b>Earned Badges:</b>", normal_style))
            badge_data = [["Badge", "Description"]]
            
            for badge in badges:
                badge_data.append([
                    f"{badge.get('icon', '')} {badge.get('name', 'Unknown')}",
                    badge.get('description', 'No description')
                ])
            
            badge_table = Table(badge_data, colWidths=[doc.width*0.3, doc.width*0.7])
            badge_table.setStyle(TableStyle([
                # Header styling - matching the general report
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightsteelblue),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.darkslategray),
                ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
                
                # Cell styling
                ('ALIGN', (0, 1), (0, -1), 'LEFT'),
                ('ALIGN', (1, 1), (1, -1), 'LEFT'),
                ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
                ('FONTNAME', (1, 1), (1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 10),
                
                # Alternating row colors - using light colors as in general report
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.Color(0.95, 0.95, 0.95)]),
                
                # Borders - matching the general report
                ('BOX', (0, 0), (-1, -1), 1, colors.darkgrey),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.lightgrey),
            ]))
            elements.append(badge_table)
            elements.append(Spacer(1, 0.5*cm))
        
        # Add awards if available
        if awards:
            elements.append(Paragraph("<b>Company Awards:</b>", normal_style))
            award_data = [["Award Type", "Date", "Reward Points"]]
            
            for award in awards:
                award_data.append([
                    award.get('awardType', 'Unknown'),
                    format_date(award.get('awardDate', '')),
                    f"{award.get('rewardPoints', 0):,}"
                ])
            
            award_table = Table(award_data, colWidths=[doc.width*0.4, doc.width*0.3, doc.width*0.3])
            award_table.setStyle(TableStyle([
                # Header styling - matching the general report
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightsteelblue),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.darkslategray),
                ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
                
                # Cell styling
                ('ALIGN', (0, 1), (0, -1), 'LEFT'),
                ('ALIGN', (1, 1), (1, -1), 'CENTER'),
                ('ALIGN', (2, 1), (2, -1), 'RIGHT'),
                ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
                ('FONTNAME', (1, 1), (2, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 10),
                
                # Alternating row colors - matching the general report
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.Color(0.95, 0.95, 0.95)]),
                
                # Borders - matching the general report
                ('BOX', (0, 0), (-1, -1), 1, colors.darkgrey),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.lightgrey),
                
                # Special styling for points
                ('TEXTCOLOR', (2, 1), (2, -1), colors.darkblue),
            ]))
            elements.append(award_table)
            elements.append(Spacer(1, 0.5*cm))
    
    # Leave History
    leave_history = data.get('leaveHistory', [])
    if leave_history:
        elements.append(Paragraph("Leave History", section_header_style))
        
        leave_data = [["Leave Type", "Duration", "Period"]]
        
        for leave in leave_history:
            start_date = format_date(leave.get('startDate', ''))
            end_date = format_date(leave.get('endDate', ''))
            leave_data.append([
                leave.get('leaveType', 'Unknown'),
                f"{leave.get('numberOfDays', 0)} days",
                f"{start_date} to {end_date}"
            ])
        
        leave_table = Table(leave_data, colWidths=[doc.width*0.3, doc.width*0.2, doc.width*0.5])
        leave_table.setStyle(TableStyle([
            # Header styling - matching the general report
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightsteelblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.darkslategray),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            
            # Cell styling
            ('ALIGN', (0, 1), (0, -1), 'LEFT'),
            ('ALIGN', (1, 1), (1, -1), 'CENTER'),
            ('ALIGN', (2, 1), (2, -1), 'LEFT'),
            ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 1), (2, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            
            # Alternating row colors - matching the general report
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.Color(0.95, 0.95, 0.95)]),
            
            # Borders - matching the general report
            ('BOX', (0, 0), (-1, -1), 1, colors.darkgrey),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.lightgrey),
        ]))
        elements.append(leave_table)
    
    # Add footer to every page
    def add_footer(canvas, doc):
        canvas.saveState()
        # Draw a line
        canvas.setStrokeColor(colors.lightgrey)
        canvas.line(doc.leftMargin, 0.75*inch, doc.width + doc.leftMargin, 0.75*inch)
        
        # Add company name
        canvas.setFont('Helvetica', 8)
        canvas.setFillColor(colors.grey)
        canvas.drawCentredString(doc.width/2 + doc.leftMargin, 0.5*inch, company_name)
        
        # Add page number
        canvas.drawRightString(doc.width + doc.leftMargin, 0.5*inch, f"Page {doc.page}")
        
        # Add confidential text
        canvas.drawString(doc.leftMargin, 0.5*inch, "CONFIDENTIAL")
        
        canvas.restoreState()

     # Build the PDF
    doc.build(elements)
    return output_pdf

