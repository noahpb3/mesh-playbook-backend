import os
from datetime import datetime
from fpdf import FPDF
import plotly.graph_objects as go
from PyPDF2 import PdfMerger

# MESH Brand Colors
MESH_BURGUNDY = (80, 20, 30)      # Primary headings
MESH_ORANGE = (240, 100, 60)       # Accent color
MESH_DARK_RED = (120, 30, 40)     # Callouts, important items
MESH_GOLD = (255, 180, 0)          # Highlights
MESH_LIGHT_GRAY = (230, 230, 240)  # Backgrounds
MESH_BLACK = (0, 0, 0)             # Body text
MESH_GRAY = (100, 100, 100)        # Secondary text

class MESHBrandedPDF(FPDF):
    def __init__(self, company_name):
        super().__init__()
        self.company_name = company_name
        self.set_auto_page_break(auto=True, margin=15)
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.logo_path = os.path.join(base_dir, 'branding', 'mesh-logo.png')
        
    def header(self):
        # Add MESH logo in top left corner on all pages
        if os.path.exists(self.logo_path):
            self.image(self.logo_path, x=10, y=8, w=30)
        
        if self.page_no() > 1:
            self.set_font('Arial', 'I', 9)
            self.set_text_color(*MESH_GRAY)
            self.set_xy(150, 10)
            self.cell(0, 10, f'{self.company_name} - AI Implementation Guide', 0, 0, 'R')
            self.ln(15)
        else:
            self.ln(20)
        
    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(*MESH_GRAY)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')
        
    def chapter_title(self, title):
        self.set_font('Arial', 'B', 18)
        self.set_text_color(*MESH_BURGUNDY)
        self.cell(0, 12, title, 0, 1, 'L')
        self.ln(3)
        
    def section_title(self, title):
        self.set_font('Arial', 'B', 14)
        self.set_text_color(*MESH_BURGUNDY)
        self.cell(0, 9, title, 0, 1, 'L')
        self.ln(2)
        
    def subsection_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.set_text_color(*MESH_DARK_RED)
        self.cell(0, 8, title, 0, 1, 'L')
        self.ln(2)
        
    def body_text(self, text):
        self.set_font('Arial', '', 10)
        self.set_text_color(*MESH_BLACK)
        self.multi_cell(0, 5, text)
        self.ln(2)
        
    def bullet_point(self, text, indent=5):
        self.set_font('Arial', '', 10)
        self.set_text_color(*MESH_BLACK)
        x_start = self.get_x()
        self.set_x(x_start + indent)
        self.set_text_color(*MESH_ORANGE)
        self.cell(4, 5, chr(149), 0, 0)
        self.set_text_color(*MESH_BLACK)
        self.set_x(x_start + indent + 4)
        self.multi_cell(0, 5, text)
        self.set_x(x_start)
        
    def accent_box(self, title, content_lines):
        """Create an accented box with MESH branding"""
        # Calculate height
        box_height = 10 + (len(content_lines) * 6) + 8
        
        # Check if we need new page
        if self.get_y() + box_height > 270:
            self.add_page()
        
        box_y = self.get_y()
        
        # Draw colored border
        self.set_draw_color(*MESH_ORANGE)
        self.set_line_width(0.8)
        self.rect(10, box_y, 190, box_height, 'D')
        
        # Add accent bar on left
        self.set_fill_color(*MESH_ORANGE)
        self.rect(10, box_y, 3, box_height, 'F')
        
        # Title
        self.set_xy(18, box_y + 5)
        self.set_font('Arial', 'B', 12)
        self.set_text_color(*MESH_DARK_RED)
        self.cell(0, 6, title, 0, 1)
        
        # Content
        self.set_x(18)
        self.set_font('Arial', '', 10)
        self.set_text_color(*MESH_BLACK)
        for line in content_lines:
            self.set_x(18)
            self.multi_cell(174, 5, line)
        
        self.ln(box_height - (self.get_y() - box_y) + 5)
        self.set_line_width(0.2)  # Reset line width

def create_mesh_branded_chart(dimension_scores):
    """Create radar chart with MESH brand colors"""
    categories = ['Strategy &\nVision', 'Data &\nSystems', 'People &\nSkills', 
                  'Governance &\nEthics', 'Execution &\nImpact']
    
    values = [
        dimension_scores.get('strategyVision', 0),
        dimension_scores.get('dataSystems', 0),
        dimension_scores.get('peopleSkills', 0),
        dimension_scores.get('governanceEthics', 0),
        dimension_scores.get('executionImpact', 0)
    ]
    
    fig = go.Figure(data=go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        line=dict(color='rgb(240, 100, 60)', width=3),  # MESH Orange
        fillcolor='rgba(240, 100, 60, 0.3)'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                gridcolor='rgb(200, 200, 200)'
            ),
            angularaxis=dict(
                gridcolor='rgb(200, 200, 200)'
            )
        ),
        showlegend=False,
        width=500,
        height=350,
        margin=dict(l=60, r=60, t=30, b=30),
        paper_bgcolor='white',
        plot_bgcolor='white'
    )
    
    chart_path = f'/tmp/mesh_chart_{datetime.now().timestamp()}.png'
    fig.write_image(chart_path)
    return chart_path

def generate_mesh_branded_addendum(session_data):
    """Generate MESH-branded custom addendum"""
    
    company_name = session_data.get('companyName', 'Your Company')
    readiness = session_data.get('readiness', {})
    toolbox = session_data.get('toolbox', {})
    strategic = session_data.get('strategic', {})
    
    # Extract data
    overall_score = readiness.get('overallScore', 0)
    maturity_level = readiness.get('maturityLevel', 'Exploring')
    maturity_desc = readiness.get('maturityDescription', '')
    dimension_scores = readiness.get('dimensionScores', {})
    dimension_details = readiness.get('dimensionDetails', {})
    recommendations = readiness.get('recommendations', {})
    
    industry = toolbox.get('industry', 'N/A')
    company_size = toolbox.get('companySize', 'N/A')
    budget = toolbox.get('budgetRange', 'N/A')
    implementation_guidance = toolbox.get('implementationGuidance', '')
    recommended_tools = toolbox.get('recommendedTools', [])
    next_steps = toolbox.get('nextSteps', [])
    
    timeline = strategic.get('timeline', 'Standard (3-6 months)')
    primary_driver = strategic.get('primaryDriver', 'Improve operations')
    
    # Create PDF
    pdf = MESHBrandedPDF(company_name)
    
    # Create branded chart
    chart_path = create_mesh_branded_chart(dimension_scores)
    
    # ===== COVER PAGE =====
    pdf.add_page()
    pdf.ln(60)
    
    pdf.set_font('Arial', 'B', 28)
    pdf.set_text_color(*MESH_BURGUNDY)
    pdf.cell(0, 14, 'Your Personalized', 0, 1, 'C')
    pdf.cell(0, 14, 'AI Implementation Guide', 0, 1, 'C')
    pdf.ln(15)
    
    # Company name with orange accent
    pdf.set_font('Arial', 'B', 20)
    pdf.set_text_color(*MESH_ORANGE)
    pdf.cell(0, 12, company_name, 0, 1, 'C')
    pdf.ln(25)
    
    # Description box
    pdf.set_font('Arial', '', 11)
    pdf.set_text_color(*MESH_BLACK)
    pdf.set_x(30)
    pdf.multi_cell(150, 6, 
        'This personalized guide is based on your AI Readiness Assessment and '
        'MESH AI Toolbox Recommendations. It provides customized insights, tool '
        'recommendations, and an action plan tailored to your organization.',
        0, 'C')
    pdf.ln(30)
    
    # Powered by MESH
    pdf.set_font('Arial', 'I', 10)
    pdf.set_text_color(*MESH_GRAY)
    pdf.cell(0, 6, 'Powered by MESH', 0, 1, 'C')
    pdf.set_font('Arial', 'I', 9)
    pdf.cell(0, 5, 'whenwemesh.com', 0, 1, 'C')
    pdf.ln(10)
    pdf.set_font('Arial', 'I', 9)
    pdf.cell(0, 6, f'Generated: {datetime.now().strftime("%B %d, %Y")}', 0, 1, 'C')
    
    # ===== YOUR AI READINESS PROFILE =====
    pdf.add_page()
    pdf.chapter_title('Your AI Readiness Profile')
    
    # Summary section
    pdf.set_font('Arial', 'B', 12)
    pdf.set_text_color(*MESH_DARK_RED)
    pdf.cell(0, 7, 'Assessment Summary', 0, 1)
    pdf.ln(2)
    
    pdf.set_font('Arial', '', 11)
    pdf.set_text_color(*MESH_BLACK)
    pdf.cell(50, 6, 'Overall Score:', 0, 0)
    pdf.set_font('Arial', 'B', 11)
    pdf.set_text_color(*MESH_ORANGE)
    pdf.cell(0, 6, f'{overall_score}/100', 0, 1)
    
    pdf.set_font('Arial', '', 11)
    pdf.set_text_color(*MESH_BLACK)
    pdf.cell(50, 6, 'Maturity Stage:', 0, 0)
    pdf.set_font('Arial', 'B', 11)
    pdf.set_text_color(*MESH_ORANGE)
    pdf.cell(0, 6, maturity_level, 0, 1)
    pdf.ln(3)
    
    if maturity_desc:
        pdf.set_font('Arial', 'I', 10)
        pdf.set_text_color(*MESH_DARK_RED)
        pdf.multi_cell(0, 5, f'"{maturity_desc}"')
        pdf.set_text_color(*MESH_BLACK)
        pdf.ln(3)
    
    pdf.ln(3)
    
    # Add branded chart
    if os.path.exists(chart_path):
        pdf.image(chart_path, x=30, w=150)
        pdf.ln(5)
    
    pdf.section_title('Your Dimension Scores')
    pdf.body_text(
        'Your assessment evaluated five critical dimensions of AI readiness. Here\'s how you scored:'
    )
    pdf.ln(2)
    
    dimension_names = {
        'strategyVision': 'Strategy & Vision',
        'dataSystems': 'Data & Systems',
        'peopleSkills': 'People & Skills',
        'governanceEthics': 'Governance & Ethics',
        'executionImpact': 'Execution & Impact'
    }
    
    for key, name in dimension_names.items():
        score = dimension_scores.get(key, 0)
        detail = dimension_details.get(key, '')
        
        pdf.set_font('Arial', 'B', 11)
        pdf.set_text_color(*MESH_DARK_RED)
        pdf.cell(0, 6, f'{name}: {score}/100', 0, 1)
        
        if detail:
            pdf.set_font('Arial', '', 10)
            pdf.set_text_color(*MESH_BLACK)
            pdf.multi_cell(0, 5, detail)
        pdf.ln(2)
    
    # ===== YOUR STRATEGIC PROFILE =====
    pdf.add_page()
    pdf.chapter_title('Your Strategic Profile')
    
    pdf.body_text(
        f'Based on the strategic questions you answered, here is {company_name}\'s AI implementation profile:'
    )
    pdf.ln(3)
    
    pdf.subsection_title('Company Overview')
    pdf.bullet_point(f'Industry: {industry}')
    pdf.bullet_point(f'Company Size: {company_size}')
    pdf.bullet_point(f'Budget Range: {budget}')
    pdf.bullet_point(f'Implementation Timeline: {timeline}')
    pdf.bullet_point(f'Primary Driver: {primary_driver}')
    pdf.ln(5)
    
    if implementation_guidance:
        pdf.subsection_title('Implementation Guidance')
        pdf.set_font('Arial', 'I', 10)
        pdf.set_text_color(*MESH_DARK_RED)
        pdf.multi_cell(0, 6, f'"{implementation_guidance}"')
        pdf.set_text_color(*MESH_BLACK)
        pdf.ln(5)
    
    # ===== YOUR RECOMMENDED AI TOOLKIT =====
    pdf.add_page()
    pdf.chapter_title('Your Recommended AI Toolkit')
    
    pdf.body_text(
        f'Based on {company_name}\'s profile, readiness score, and business objectives, we recommend '
        f'the following AI tools as your ideal starting point. These {len(recommended_tools)} tools have been '
        f'selected to match your industry, budget, and implementation goals.'
    )
    pdf.ln(5)
    
    # Group tools by priority
    essential = [t for t in recommended_tools if t.get('priority') == 'ESSENTIAL']
    recommended_list = [t for t in recommended_tools if t.get('priority') == 'RECOMMENDED']
    optional = [t for t in recommended_tools if t.get('priority') == 'OPTIONAL']
    
    for priority_label, tools in [('Essential Tools', essential), 
                                   ('Recommended Tools', recommended_list), 
                                   ('Optional Tools', optional)]:
        if tools:
            pdf.subsection_title(priority_label)
            
            for tool in tools:
                if pdf.get_y() > 240:
                    pdf.add_page()
                
                # Tool name with orange accent
                pdf.set_font('Arial', 'B', 13)
                pdf.set_text_color(*MESH_ORANGE)
                pdf.cell(0, 7, f'{tool.get("name", "Tool")}', 0, 1)
                
                pdf.set_font('Arial', '', 10)
                pdf.set_text_color(*MESH_GRAY)
                pdf.cell(0, 5, f'Category: {tool.get("category", "N/A")} | Match Score: {tool.get("matchScore", 0)}/100', 0, 1)
                pdf.set_text_color(*MESH_BLACK)
                pdf.ln(2)
                
                # Why we recommend
                if tool.get('whyRecommend'):
                    pdf.set_font('Arial', 'B', 10)
                    pdf.set_text_color(*MESH_DARK_RED)
                    pdf.cell(0, 5, 'Why We Recommend:', 0, 1)
                    pdf.set_font('Arial', '', 10)
                    pdf.set_text_color(*MESH_BLACK)
                    for reason in tool.get('whyRecommend', []):
                        pdf.bullet_point(reason, indent=3)
                    pdf.ln(1)
                
                # Key features
                if tool.get('keyFeatures'):
                    pdf.set_font('Arial', 'B', 10)
                    pdf.set_text_color(*MESH_DARK_RED)
                    pdf.cell(0, 5, 'Key Features:', 0, 1)
                    pdf.set_font('Arial', '', 10)
                    pdf.set_text_color(*MESH_BLACK)
                    for feature in tool.get('keyFeatures', [])[:5]:
                        pdf.bullet_point(feature, indent=3)
                    pdf.ln(1)
                
                # Pricing
                if tool.get('pricing'):
                    pdf.set_font('Arial', 'B', 10)
                    pdf.set_text_color(*MESH_DARK_RED)
                    pdf.cell(0, 5, 'Pricing:', 0, 1)
                    pdf.set_font('Arial', '', 10)
                    pdf.set_text_color(*MESH_BLACK)
                    for price in tool.get('pricing', []):
                        pdf.bullet_point(price, indent=3)
                    pdf.ln(1)
                
                # Website
                if tool.get('website'):
                    pdf.set_font('Arial', 'I', 9)
                    pdf.set_text_color(*MESH_ORANGE)
                    pdf.cell(0, 5, f'Website: {tool.get("website")}', 0, 1)
                    pdf.set_text_color(*MESH_BLACK)
                
                pdf.ln(5)
    
    # ===== YOUR PERSONALIZED ACTION PLAN =====
    pdf.add_page()
    pdf.chapter_title('Your Personalized Action Plan')
    
    pdf.body_text(
        f'This action plan combines insights from your AI Readiness Assessment with the recommended tools '
        f'to create a clear roadmap for {company_name}\'s AI implementation journey.'
    )
    pdf.ln(5)
    
    # Immediate next steps in accent box
    if next_steps:
        pdf.section_title('Immediate Next Steps')
        pdf.body_text('Start your AI journey with these concrete actions:')
        pdf.ln(2)
        
        for i, step in enumerate(next_steps, 1):
            pdf.set_font('Arial', 'B', 11)
            pdf.set_text_color(*MESH_ORANGE)
            pdf.cell(8, 6, f'{i}.', 0, 0)
            pdf.set_font('Arial', '', 10)
            pdf.set_text_color(*MESH_BLACK)
            pdf.multi_cell(0, 6, step)
            pdf.ln(1)
        pdf.ln(3)
    
    # High priority recommendations
    high_priority = recommendations.get('high', [])
    if high_priority:
        pdf.section_title('High Priority Recommendations')
        pdf.body_text(
            'Based on your assessment scores, these are the most critical areas to address:'
        )
        pdf.ln(2)
        
        for rec in high_priority[:4]:
            if pdf.get_y() > 230:
                pdf.add_page()
            
            pdf.set_font('Arial', 'B', 12)
            pdf.set_text_color(*MESH_DARK_RED)
            title = rec.get('title', 'Recommendation')
            if rec.get('dimension'):
                title += f' ({rec.get("dimension")})'
            pdf.cell(0, 6, title, 0, 1)
            pdf.set_text_color(*MESH_BLACK)
            
            if rec.get('description'):
                pdf.set_font('Arial', '', 10)
                pdf.multi_cell(0, 5, rec.get('description'))
                pdf.ln(1)
            
            if rec.get('actionItems'):
                pdf.set_font('Arial', 'B', 9)
                pdf.set_text_color(*MESH_DARK_RED)
                pdf.cell(0, 5, 'Action Items:', 0, 1)
                pdf.set_font('Arial', '', 9)
                pdf.set_text_color(*MESH_BLACK)
                for action in rec.get('actionItems', []):
                    pdf.bullet_point(action, indent=3)
            
            pdf.ln(3)
    
    # Medium priority recommendations
    medium_priority = recommendations.get('medium', [])
    if medium_priority:
        if pdf.get_y() > 200:
            pdf.add_page()
        
        pdf.section_title('Medium Priority Recommendations')
        pdf.body_text('Once high-priority items are underway, focus on these areas:')
        pdf.ln(2)
        
        for rec in medium_priority[:3]:
            if pdf.get_y() > 230:
                pdf.add_page()
            
            pdf.set_font('Arial', 'B', 11)
            pdf.set_text_color(*MESH_DARK_RED)
            title = rec.get('title', 'Recommendation')
            if rec.get('dimension'):
                title += f' ({rec.get("dimension")})'
            pdf.cell(0, 6, title, 0, 1)
            pdf.set_text_color(*MESH_BLACK)
            
            if rec.get('description'):
                pdf.set_font('Arial', '', 10)
                pdf.multi_cell(0, 5, rec.get('description'))
            
            pdf.ln(3)
    
    # Save addendum PDF
    addendum_path = f'/tmp/mesh_branded_addendum_{datetime.now().timestamp()}.pdf'
    pdf.output(addendum_path)
    
    # Clean up chart
    if os.path.exists(chart_path):
        os.remove(chart_path)
    
    return addendum_path

def merge_playbook_with_addendum(base_pdf_path, addendum_pdf_path, output_path):
    """Merge the base playbook with custom addendum"""
    merger = PdfMerger()
    
    # Add custom addendum first (personalized pages)
    merger.append(addendum_pdf_path)
    
    # Add base playbook (educational content)
    merger.append(base_pdf_path)
    
    # Write merged PDF
    merger.write(output_path)
    merger.close()
    
    return output_path

def generate_complete_playbook_branded(session_data, base_pdf_path):
    """Generate complete MESH-branded playbook"""
    
    # Generate MESH-branded addendum
    addendum_path = generate_mesh_branded_addendum(session_data)
    
    # Merge with base PDF
    output_path = f'/home/ubuntu/playbook-generator/backend/output/mesh_playbook_{datetime.now().timestamp()}.pdf'
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    final_path = merge_playbook_with_addendum(base_pdf_path, addendum_path, output_path)
    
    # Clean up temporary addendum
    if os.path.exists(addendum_path):
        os.remove(addendum_path)
    
    return final_path

