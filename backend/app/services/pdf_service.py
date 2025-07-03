from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from typing import Dict, Any, List
import io
import os

class PDFService:
    """Service to generate PDF itineraries"""
    
    @staticmethod
    def generate_itinerary_pdf(itinerary_data: Dict[str, Any], 
                             selected_flight: Dict[str, Any] = None,
                             selected_hotel: Dict[str, Any] = None) -> bytes:
        """Generate PDF from itinerary data"""
        
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=0.5*inch)
        
        # Get styles
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            alignment=TA_CENTER,
            textColor=colors.HexColor('#FF6C00')
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=16,
            spaceAfter=12,
            textColor=colors.HexColor('#333333')
        )
        
        body_style = ParagraphStyle(
            'CustomBody',
            parent=styles['Normal'],
            fontSize=11,
            spaceAfter=6,
            leftIndent=20
        )
        
        # Build PDF content
        story = []
        
        # Title
        story.append(Paragraph("🇮🇳 Raahi.ai Travel Itinerary", title_style))
        story.append(Spacer(1, 20))
        
        # Trip Overview
        story.append(Paragraph(itinerary_data.get('title', 'Your Trip'), heading_style))
        story.append(Paragraph(itinerary_data.get('description', ''), body_style))
        story.append(Spacer(1, 15))
        
        # Trip Summary Table
        summary_data = [
            ['Trip Duration', f"{itinerary_data.get('total_days', 0)} days"],
            ['Estimated Cost', f"₹{itinerary_data.get('estimated_cost', 0):,.0f}"],
        ]
        
        if selected_flight:
            summary_data.append(['Flight', f"{selected_flight.get('airline', '')} - {selected_flight.get('flight_number', '')}"])
        
        if selected_hotel:
            summary_data.append(['Hotel', selected_hotel.get('name', '')])
        
        summary_table = Table(summary_data, colWidths=[2*inch, 3*inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#FF6C00')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(summary_table)
        story.append(Spacer(1, 20))
        
        # Daily Itinerary
        story.append(Paragraph("Daily Itinerary", heading_style))
        
        for day_plan in itinerary_data.get('daily_plans', []):
            # Day header
            day_title = f"Day {day_plan.get('day', 1)}: {day_plan.get('title', '')}"
            story.append(Paragraph(day_title, heading_style))
            story.append(Paragraph(f"Date: {day_plan.get('date', '')}", body_style))
            story.append(Spacer(1, 10))
            
            # Activities table
            activities_data = [['Time', 'Activity', 'Duration']]
            
            for activity in day_plan.get('activities', []):
                activities_data.append([
                    activity.get('time', ''),
                    f"{activity.get('icon', '')} {activity.get('activity', '')}",
                    activity.get('duration', '')
                ])
            
            activities_table = Table(activities_data, colWidths=[1*inch, 3.5*inch, 1*inch])
            activities_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#F0F0F0')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('FONTSIZE', (0, 1), (-1, -1), 9),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('VALIGN', (0, 0), (-1, -1), 'TOP')
            ]))
            
            story.append(activities_table)
            story.append(Spacer(1, 15))
        
        # Footer
        story.append(Spacer(1, 30))
        footer_style = ParagraphStyle(
            'Footer',
            parent=styles['Normal'],
            fontSize=10,
            alignment=TA_CENTER,
            textColor=colors.grey
        )
        story.append(Paragraph("Generated by Raahi.ai - Your AI Travel Companion", footer_style))
        story.append(Paragraph("Visit us at raahi.ai for more amazing travel experiences", footer_style))
        
        # Build PDF
        doc.build(story)
        
        # Get PDF bytes
        pdf_bytes = buffer.getvalue()
        buffer.close()
        
        return pdf_bytes