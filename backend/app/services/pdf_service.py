from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from typing import Dict, Any, List, Optional
import io
import os
from datetime import datetime

class PDFService:
    """Service to generate professional PDF itineraries"""
    
    @staticmethod
    def generate_itinerary_pdf(
        itinerary_data: Dict[str, Any], 
        selected_flight: Optional[Dict[str, Any]] = None,
        selected_hotel: Optional[Dict[str, Any]] = None,
        session_data: Optional[Dict[str, Any]] = None
    ) -> bytes:
        """Generate a professional PDF from itinerary data"""
        
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer, 
            pagesize=A4, 
            topMargin=0.75*inch,
            bottomMargin=0.75*inch,
            leftMargin=0.75*inch,
            rightMargin=0.75*inch
        )
        
        # Get styles
        styles = getSampleStyleSheet()
        
        # Custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=28,
            spaceAfter=20,
            alignment=TA_CENTER,
            textColor=colors.HexColor('#FF6C00'),
            fontName='Helvetica-Bold'
        )
        
        subtitle_style = ParagraphStyle(
            'CustomSubtitle',
            parent=styles['Heading2'],
            fontSize=16,
            spaceAfter=15,
            alignment=TA_CENTER,
            textColor=colors.HexColor('#666666'),
            fontName='Helvetica'
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=18,
            spaceAfter=12,
            spaceBefore=12,
            textColor=colors.HexColor('#333333'),
            fontName='Helvetica-Bold'
        )
        
        subheading_style = ParagraphStyle(
            'CustomSubheading',
            parent=styles['Heading3'],
            fontSize=14,
            spaceAfter=8,
            spaceBefore=8,
            textColor=colors.HexColor('#444444'),
            fontName='Helvetica-Bold'
        )
        
        body_style = ParagraphStyle(
            'CustomBody',
            parent=styles['Normal'],
            fontSize=11,
            spaceAfter=6,
            leading=14,
            textColor=colors.HexColor('#333333'),
            fontName='Helvetica'
        )
        
        # Build PDF content
        story = []
        
        # Header with Indian flag colors
        story.append(Paragraph("🇮🇳 Raahi.ai Travel Itinerary", title_style))
        story.append(Paragraph("Your AI-Powered Journey Through Incredible India", subtitle_style))
        story.append(Spacer(1, 30))
        
        # Trip Overview
        trip_title = itinerary_data.get('title', 'Your Amazing Journey')
        story.append(Paragraph(trip_title, heading_style))
        
        trip_description = itinerary_data.get('description', '')
        if trip_description:
            story.append(Paragraph(trip_description, body_style))
        
        story.append(Spacer(1, 20))
        
        # Trip Summary Table
        summary_data = [
            ['Trip Duration', f"{itinerary_data.get('total_days', 0)} days"],
            ['Estimated Cost', f"₹{itinerary_data.get('estimated_cost', 0):,.0f}"],
            ['Generated On', datetime.now().strftime('%B %d, %Y')],
        ]
        
        if selected_flight:
            summary_data.append([
                'Flight', 
                f"{selected_flight.get('airline', '')} {selected_flight.get('flight_number', '')}"
            ])
        
        if selected_hotel:
            summary_data.append([
                'Hotel', 
                selected_hotel.get('name', '')
            ])
        
        summary_table = Table(summary_data, colWidths=[2.5*inch, 3.5*inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#FF6C00')),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.whitesmoke),
            ('BACKGROUND', (1, 0), (1, -1), colors.HexColor('#FFF8F0')),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#E0E0E0'))
        ]))
        
        story.append(summary_table)
        story.append(Spacer(1, 30))
        
        # Flight Details (if selected)
        if selected_flight:
            story.append(Paragraph("✈️ Flight Details", heading_style))
            
            flight_data = [
                ['Airline', selected_flight.get('airline', '')],
                ['Flight Number', selected_flight.get('flight_number', '')],
                ['Route', f"{selected_flight.get('departure_airport', '')} → {selected_flight.get('arrival_airport', '')}"],
                ['Departure', f"{selected_flight.get('departure_date', '')} at {selected_flight.get('departure_time', '')}"],
                ['Arrival', f"{selected_flight.get('departure_date', '')} at {selected_flight.get('arrival_time', '')}"],
                ['Duration', selected_flight.get('duration', '')],
                ['Class', selected_flight.get('flight_class', '').title()],
                ['Price', f"₹{selected_flight.get('price', 0):,.0f}"]
            ]
            
            flight_table = Table(flight_data, colWidths=[2*inch, 4*inch])
            flight_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#F0F8FF')),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('PADDING', (0, 0), (-1, -1), 6),
                ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#E0E0E0'))
            ]))
            
            story.append(flight_table)
            story.append(Spacer(1, 20))
        
        # Hotel Details (if selected)
        if selected_hotel:
            story.append(Paragraph("🏨 Hotel Details", heading_style))
            
            hotel_data = [
                ['Hotel Name', selected_hotel.get('name', '')],
                ['Location', selected_hotel.get('location', '')],
                ['Rating', f"⭐ {selected_hotel.get('rating', 0)}/5.0"],
                ['Reviews', f"{selected_hotel.get('reviews_count', 0)} reviews"],
                ['Price per Night', f"₹{selected_hotel.get('price_per_night', 0):,.0f}"],
            ]
            
            # Add amenities
            amenities = selected_hotel.get('amenities', [])
            if amenities:
                amenity_list = ', '.join([a.get('label', '') for a in amenities[:5]])
                hotel_data.append(['Key Amenities', amenity_list])
            
            hotel_table = Table(hotel_data, colWidths=[2*inch, 4*inch])
            hotel_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#F0FFF0')),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('PADDING', (0, 0), (-1, -1), 6),
                ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#E0E0E0'))
            ]))
            
            story.append(hotel_table)
            story.append(Spacer(1, 20))
        
        # Daily Itinerary
        story.append(Paragraph("📅 Detailed Daily Itinerary", heading_style))
        story.append(Spacer(1, 15))
        
        for day_plan in itinerary_data.get('daily_plans', []):
            # Day header
            day_title = f"Day {day_plan.get('day', 1)}: {day_plan.get('title', '')}"
            story.append(Paragraph(day_title, subheading_style))
            
            date_info = f"📅 {day_plan.get('date', '')} • Estimated Cost: ₹{day_plan.get('estimated_cost', 0):,.0f}"
            story.append(Paragraph(date_info, body_style))
            story.append(Spacer(1, 8))
            
            # Activities table
            activities_data = [['Time', 'Activity', 'Duration', 'Cost']]
            
            for activity in day_plan.get('activities', []):
                cost = activity.get('cost', 0)
                cost_str = f"₹{cost:,.0f}" if cost > 0 else "Free"
                
                activities_data.append([
                    activity.get('time', ''),
                    f"{activity.get('icon', '')} {activity.get('activity', '')}",
                    activity.get('duration', ''),
                    cost_str
                ])
            
            activities_table = Table(activities_data, colWidths=[1*inch, 3*inch, 1*inch, 1*inch])
            activities_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#FF6C00')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('FONTSIZE', (0, 1), (-1, -1), 9),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('ALIGN', (3, 0), (3, -1), 'RIGHT'),  # Align cost column to right
                ('PADDING', (0, 0), (-1, -1), 6),
                ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#E0E0E0')),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F9F9F9')])
            ]))
            
            story.append(activities_table)
            story.append(Spacer(1, 20))
        
        # AI Insights (if available)
        ai_insights = itinerary_data.get('ai_insights', {})
        if ai_insights:
            story.append(Paragraph("🤖 AI Travel Insights", heading_style))
            
            for insight_key, insight_value in ai_insights.items():
                if insight_value:
                    # Format the key as a readable title
                    title = insight_key.replace('_', ' ').title()
                    story.append(Paragraph(f"<b>{title}:</b> {insight_value}", body_style))
                    story.append(Spacer(1, 6))
            
            story.append(Spacer(1, 15))
        
        # Important Notes
        story.append(Paragraph("📋 Important Notes", heading_style))
        
        notes = [
            "• All costs are estimates in Indian Rupees (₹) and may vary based on season and availability",
            "• Flight and hotel bookings are not confirmed through this itinerary - use provided booking links",
            "• Check visa requirements, weather conditions, and local guidelines before travel",
            "• Keep digital and physical copies of important documents",
            "• Consider travel insurance for a worry-free journey"
        ]
        
        for note in notes:
            story.append(Paragraph(note, body_style))
        
        story.append(Spacer(1, 30))
        
        # Footer
        footer_style = ParagraphStyle(
            'Footer',
            parent=styles['Normal'],
            fontSize=10,
            alignment=TA_CENTER,
            textColor=colors.HexColor('#666666'),
            fontName='Helvetica'
        )
        
        story.append(Paragraph("Generated by Raahi.ai - Your AI-Powered Travel Companion", footer_style))
        story.append(Paragraph("Visit raahi.ai for more amazing travel experiences • Safe travels! 🙏", footer_style))
        
        # Build PDF
        doc.build(story)
        
        # Get PDF bytes
        pdf_bytes = buffer.getvalue()
        buffer.close()
        
        return pdf_bytes
    
    @staticmethod
    def generate_simple_itinerary_pdf(itinerary_data: Dict[str, Any]) -> bytes:
        """Generate a simple PDF without booking details"""
        
        return PDFService.generate_itinerary_pdf(
            itinerary_data=itinerary_data,
            selected_flight=None,
            selected_hotel=None,
            session_data=None
        )