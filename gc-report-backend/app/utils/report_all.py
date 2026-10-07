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

def format_date(date_input):
    """Format date string or datetime object to readable format"""
    try:
        # If it's already a datetime object
        if isinstance(date_input, datetime):
            return date_input.strftime('%b %d, %Y')
        
        # If it's a string, try to parse it
        date_str = str(date_input)
        date_obj = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        return date_obj.strftime('%b %d, %Y')
    except:
        # Return as string if parsing fails
        return str(date_input)

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

def create_report(data, output_pdf, pagesize=A4):
    """
    Create general employee mood report PDF from data dictionary
    """
    # Create the PDF document
    doc = SimpleDocTemplate(
        output_pdf,
        pagesize=pagesize,
        leftMargin=1.2*cm,  # Reduced margins to use more space
        rightMargin=1.2*cm,
        topMargin=1.5*cm,
        bottomMargin=1.5*cm
    )
    
    # Create styles
    styles = getSampleStyleSheet()
    
    # Create custom styles with unique names
    title_style = ParagraphStyle(
        name='CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        alignment=TA_CENTER,
        spaceAfter=10,  # Reduced spacing
        textColor=colors.darkblue
    )
    
    subtitle_style = ParagraphStyle(
        name='CustomSubtitle',
        parent=styles['Heading2'],
        fontSize=18,
        textColor=colors.navy,
        spaceAfter=8  # Reduced spacing
    )
    
    section_header_style = ParagraphStyle(
        name='SectionHeader',
        parent=styles['Heading3'],
        fontSize=16,
        textColor=colors.darkblue,
        spaceBefore=12,  # Reduced spacing
        spaceAfter=8
    )
    
    normal_style = ParagraphStyle(
        name='CustomNormal',
        parent=styles['Normal'],
        fontSize=10,
        spaceBefore=4,  # Reduced spacing
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
    
    # Elements to build the PDF
    elements = []
    
    # Add title
    elements.append(Paragraph(f"Employee Mood Report", title_style))
    
    # Add date
    date_string = datetime.now().strftime("%B %d, %Y")
    elements.append(Paragraph(f"Generated on: {date_string}", normal_style))
    elements.append(Spacer(1, 0.7*cm))  
    
    # Key Metrics section
    elements.append(Paragraph("Key Metrics", section_header_style))
    elements.append(Spacer(1, 0.5*cm))  

    
    # Create a table for key metrics
    happy_percentage = int((data.get('noOfHappyEmp', 0) / data.get('totalNumberOfEmp', 1)) * 100)
    
    metrics_data = [
        [
            Paragraph("Total Employees", metric_title_style),
            Paragraph("Happy Employees", metric_title_style),
            Paragraph("Happiness Rate", metric_title_style),
            Paragraph("Escalated Issues", metric_title_style)
        ],
        [
            Paragraph(f"{data.get('totalNumberOfEmp', 0):,}", metric_value_style),
            Paragraph(f"{data.get('noOfHappyEmp', 0):,}", metric_value_style),
            Paragraph(f"{happy_percentage}%", metric_value_style),
            Paragraph(f"{data.get('noOfEscalatedIssues', 0):,}", metric_value_style)
        ]
    ]
    
    metrics_table = Table(metrics_data, colWidths=[doc.width/4, doc.width/4, doc.width/4, doc.width/4])
    metrics_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (3, 0), colors.lightsteelblue),
        ('BACKGROUND', (0, 1), (0, 1), colors.lavender),
        ('BACKGROUND', (1, 1), (1, 1), colors.lightgreen),
        ('BACKGROUND', (2, 1), (2, 1), colors.lightcyan),
        ('BACKGROUND', (3, 1), (3, 1), colors.mistyrose),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),  # Slightly reduced padding
        ('TOPPADDING', (0, 0), (-1, -1), 12),
        ('BOX', (0, 0), (-1, -1), 1, colors.darkgrey),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.lightgrey),
    ]))
    elements.append(metrics_table)
    elements.append(Spacer(1, 0.6*cm))  # Reduced spacing
    
    # Chat Interactions & Growth
    chat_metrics_data = [
        [
            Paragraph("Total Chat Interactions", metric_title_style),
            Paragraph("Growth from Previous Month", metric_title_style)
        ],
        [
            Paragraph(f"{data.get('totalChatInteractions', 0):,}", metric_value_style),
            Paragraph(f"{data.get('hikeFromPrevMonth', 0)}%", metric_value_style)
        ]
    ]
    
    chat_metrics_table = Table(chat_metrics_data, colWidths=[doc.width/2, doc.width/2])
    chat_metrics_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (1, 0), colors.lightsteelblue),
        ('BACKGROUND', (0, 1), (0, 1), colors.paleturquoise),
        ('BACKGROUND', (1, 1), (1, 1), colors.lightgreen if data.get('hikeFromPrevMonth', 0) > 0 else colors.mistyrose),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),  # Slightly reduced padding
        ('TOPPADDING', (0, 0), (-1, -1), 12),
        ('BOX', (0, 0), (-1, -1), 1, colors.darkgrey),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.lightgrey),
    ]))
    elements.append(chat_metrics_table)
    elements.append(Spacer(1, 0.8*cm))  # Reduced spacing
    
    # Employee Mood Distribution
    elements.append(Paragraph("Employee Mood Distribution", section_header_style))
    
    mood_dist = data.get('employeeMoodDistribution', {})
    
    # Prepare data for pie chart
    mood_labels = ['Happy', 'Tending to Happy', 'Neutral', 'Sad', 'Angry']
    mood_values = [
        mood_dist.get('happy', 0),
        mood_dist.get('tendingToHappy', 0),
        mood_dist.get('neutral', 0),
        mood_dist.get('sad', 0),
        mood_dist.get('angry', 0)
    ]
    
    # Calculate percentages for labels
    total = sum(mood_values)
    percentages = [0] * len(mood_values) if total == 0 else [(value / total) * 100 for value in mood_values]
    labels_with_percentages = [f"{label} ({value}, {perc:.1f}%)" for label, value, perc in zip(mood_labels, mood_values, percentages)]
    
    # Only create pie chart if there's meaningful data
    if sum(mood_values) > 0:
        # Create a bigger pie chart with percentages
        drawing = Drawing(500, 300)  # Increased size
        
        pie = Pie()
        pie.x = 150
        pie.y = 50
        pie.width = 200  # Increased size
        pie.height = 200  # Increased size
        pie.data = mood_values
        pie.labels = labels_with_percentages  # Use labels with percentages
        pie.slices.strokeWidth = 0.5
        pie.simpleLabels = 0  # Disable simple labels to use our custom ones
        # pie.labelRadius = 1.2  # Not available in all ReportLab versions
        pie.sideLabels = 1  # Put labels to the side
        
        # Add different colors for moods
        mood_colors = [colors.green, colors.limegreen, colors.gold, colors.orange, colors.red]
        for i, color in enumerate(mood_colors):
            pie.slices[i].fillColor = color
            
        # Add percentages inside slices
        for i, percent in enumerate(percentages):
            if percent > 5:  # Only show percentage for slices big enough
                x = pie.x + (pie.width/2) * 0.7 * (1 if percent < 10 else 0.8)  # Adjust position based on value
                y = pie.y + (pie.height/2) * 0.7
                text = String(x, y, f"{percent:.1f}%", textAnchor='middle')
                text.fontName = 'Helvetica-Bold'
                text.fontSize = 10
                text.fillColor = colors.white
                drawing.add(text)
                
        drawing.add(pie)
        
        # Add additional spacing to fill the bottom of the first page, but not too much
        elements.append(drawing)
        elements.append(Spacer(1, 0.5*cm))  # Reduced spacing
        
        # Add a summary box for mood distribution
        mood_summary_style = ParagraphStyle(
            name='MoodSummary',
            parent=styles['Normal'],
            fontSize=11,
            textColor=colors.darkslategray,
            backColor=colors.lightgrey,
            borderColor=colors.darkgrey,
            borderWidth=1,
            borderPadding=8,
            alignment=TA_LEFT,
            spaceBefore=8,
            spaceAfter=8,
            leftIndent=10,
            rightIndent=10
        )
        
        # Determine dominant mood
        dominant_mood_index = mood_values.index(max(mood_values)) if any(mood_values) else -1
        dominant_mood = mood_labels[dominant_mood_index] if dominant_mood_index >= 0 else "None"
        
        # Create a summary of the mood distribution
        mood_summary = f"""
        <b>Mood Distribution Summary:</b>
        
        • The dominant mood among employees is currently <b>"{dominant_mood}"</b>
        • {sum(mood_values)} employees have reported their mood
        • {percentages[0]:.1f}% of employees report being Happy
        • {percentages[3] + percentages[4]:.1f}% of employees report negative emotions (Sad or Angry)
        
        This distribution suggests that immediate attention may be required to address employee concerns
        and improve overall workplace satisfaction.
        """
        
        elements.append(Paragraph(mood_summary, mood_summary_style))
        
        # Add just enough spacing to fit content on first page without creating blank page
        elements.append(Spacer(1, 0.5*cm))
                
        # Daily Chat Participation Chart on second page
        elements.append(Paragraph("Daily Chat Participation", section_header_style))
    else:
        elements.append(Paragraph("No mood distribution data available.", normal_style))
        elements.append(PageBreak())
        elements.append(Paragraph("Daily Chat Participation", section_header_style))
    
    # Process daily chat data
    daily_chats = data.get('dailyChatParticipation', [])
    if daily_chats:
        # Sort by date
        daily_chats = sorted(daily_chats, key=lambda x: x.get('date', ''))
        
        # Extract the data
        # HERE IS THE FIX - Make sure to convert ALL datetime objects to strings
        dates = []
        for entry in daily_chats:
            date_value = entry.get('date', '')
            # Convert datetime objects to formatted strings
            formatted_date = format_date(date_value)
            dates.append(formatted_date)
        
        participants = [entry.get('numberOfParticipants', 0) for entry in daily_chats]
        
        # Create line chart
        drawing = Drawing(doc.width, 250)  # Full width
        
        chart = HorizontalLineChart()
        chart.x = 30  # Reduced margin
        chart.y = 40
        chart.height = 160
        chart.width = doc.width - 60  # Use more width
        chart.data = [participants]
        # This line was causing the error by trying to use datetime objects
        chart.categoryAxis.categoryNames = dates  # Now using properly formatted string dates
        chart.categoryAxis.labels.boxAnchor = 'ne'
        chart.categoryAxis.labels.angle = 30
        chart.categoryAxis.labels.dy = -10
        chart.categoryAxis.labels.fontSize = 8
        
        chart.valueAxis.valueMin = 0
        chart.valueAxis.valueMax = max(participants) * 1.2 if participants else 10
        chart.valueAxis.valueStep = max(1, max(participants) // 5 if participants else 2)
        
        # Add a line with markers
        chart.lines[0].strokeWidth = 2
        chart.lines[0].symbol = makeMarker('FilledCircle')
        chart.lines[0].strokeColor = colors.blue
        
        drawing.add(chart)
        elements.append(drawing)
        
        # Add analysis section for the graph using a table instead of paragraphs
        elements.append(Spacer(1, 1.8*cm))
        
        elements.append(Paragraph("Chat Participation Analysis", section_header_style))
        elements.append(Spacer(1, 0.8*cm))  # Reduced spacing

        # Calculate some metrics for analysis
        avg_participants = sum(participants) / len(participants) if participants else 0
        max_participants = max(participants) if participants else 0
        min_participants = min(participants) if participants else 0
        max_date = dates[participants.index(max_participants)] if participants else "N/A"
        min_date = dates[participants.index(min_participants)] if participants else "N/A"
        
        # Check for trends
        trend = "increasing" if len(participants) >= 3 and participants[-1] > participants[-2] > participants[-3] else \
                "decreasing" if len(participants) >= 3 and participants[-1] < participants[-2] < participants[-3] else \
                "fluctuating"
        
        # Create Key Observations table
        observations_data = [
            ["Key Metrics", "Value"],
            ["Average Daily Participation", f"{avg_participants:.1f} employees"],
            ["Highest Participation", f"{max_participants} employees on {max_date}"],
            ["Lowest Participation", f"{min_participants} employees on {min_date}"],
            ["Recent Trend", f"Participation has been {trend} over the most recent period"]
        ]
        
        observations_table = Table(observations_data, colWidths=[doc.width*0.4, doc.width*0.6])
        observations_table.setStyle(TableStyle([
            # Header styling
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            
            # Cell styling
            ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
            ('BACKGROUND', (0, 1), (0, -1), colors.lightsteelblue),
            ('BACKGROUND', (1, 1), (1, -1), colors.white),
            
            # Alignment
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            
            # Borders and padding
            ('BOX', (0, 0), (-1, -1), 1, colors.black),
            ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ]))
        
        elements.append(observations_table)
        elements.append(Spacer(1, 1.5*cm))
        
    else:
        elements.append(Paragraph("No daily chat participation data available.", normal_style))
    
    # Add a page break after Daily Chat Participation
    elements.append(PageBreak())
    
    # Escalated Issues Section
    elements.append(Paragraph("Escalated Employee Issues", section_header_style))
    elements.append(Spacer(1, 0.5*cm))
    
    escalated_users = data.get('briefEscalatedUsersList', [])
    if escalated_users:
        # Modified this section to handle the 5 cards per page requirement
        cards_per_page = 5
        total_users = len(escalated_users)
        
        for i, user in enumerate(escalated_users):
            # If we've completed a set of 5 cards and have more to go, insert a page break
            if i > 0 and i % cards_per_page == 0:
                elements.append(PageBreak())
                elements.append(Spacer(1, 2.5*cm))
            
            # Get current mood and color
            current_mood = user.get('currentMood', 'N/A')
            mood_color = create_mood_indicator(current_mood)
            
            # Create a lighter version of the mood color
            lighter_mood_color = colors.Color(
                min(1.0, mood_color.red + 0.4),
                min(1.0, mood_color.green + 0.4),
                min(1.0, mood_color.blue + 0.4)
            )
            
            # Create a card-like table for each escalated user
            card_content = [
                [
                    Paragraph(f"<b>Name:</b> {user.get('name', 'N/A')}", normal_style),
                    Paragraph(f"<b>ID:</b> {user.get('empid', 'N/A')}", normal_style),
                    Paragraph(f"<b>Department:</b> {user.get('dept', 'N/A')}", normal_style)
                ],
                [
                    Paragraph(f"<b>Current Mood:</b> {current_mood}", normal_style),
                    Paragraph(f"<b>Last Active:</b> {format_date(user.get('lastActive', 'N/A'))}", normal_style),
                    ''
                ],
                [
                    Paragraph(f"<b>Mood Summary:</b> {user.get('briefMoodSummary', 'N/A')}", normal_style),
                    '',
                    ''
                ]
            ]
            
            card_table = Table(card_content, colWidths=[doc.width/2, doc.width/4, doc.width/4])
            
            card_table.setStyle(TableStyle([
                # Use white background with colored header row
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightsteelblue),
                ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                
                # Add nice padding
                ('LEFTPADDING', (0, 0), (-1, -1), 10),
                ('RIGHTPADDING', (0, 0), (-1, -1), 10),
                ('TOPPADDING', (0, 0), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                
                # Make mood summary span all columns
                ('SPAN', (0, 2), (-1, 2)),
                
                # Border style
                ('BOX', (0, 0), (-1, -1), 1, colors.darkgrey),
                ('GRID', (0, 0), (-1, 1), 0.5, colors.lightgrey),
                
                # Color the mood cell
                ('BACKGROUND', (0, 1), (0, 1), lighter_mood_color),
                
                # Vertical alignment
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ]))
            
            elements.append(card_table)
            
            # Add spacing between cards, but not after the last card on a page
            # or not after the very last card
            if i < total_users - 1 and (i + 1) % cards_per_page != 0:
                elements.append(Spacer(1, 1*cm))
    else:
        elements.append(Paragraph("No escalated employee issues to report.", normal_style))
    
    # Build the PDF
    doc.build(elements)
    
    return output_pdf