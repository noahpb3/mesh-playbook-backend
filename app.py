from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
import json
from datetime import datetime
from text_parser import parse_text_file
from addendum_generator import generate_complete_playbook_branded

app = Flask(__name__)
CORS(app)

# Configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_PDF_PATH = os.path.join(BASE_DIR, 'AI-Implementation-Playbook.pdf')
OUTPUT_DIR = os.path.join(BASE_DIR, 'output')
os.makedirs(OUTPUT_DIR, exist_ok=True)

# In-memory session storage (for MVP)
sessions = {}

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'service': 'MESH AI Playbook Generator',
        'version': '2.0-branded',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/generate-playbook', methods=['POST'])
def generate_playbook():
    """Generate a complete MESH-branded playbook from uploaded files"""
    try:
        # Get uploaded files
        if 'readiness_file' not in request.files or 'toolbox_file' not in request.files:
            return jsonify({'error': 'Both readiness_file and toolbox_file are required'}), 400
        
        readiness_file = request.files['readiness_file']
        toolbox_file = request.files['toolbox_file']
        
        # Get form data
        company_name = request.form.get('companyName', 'Your Company')
        primary_driver = request.form.get('primaryDriver', 'Improve operations')
        risk_tolerance = request.form.get('riskTolerance', 'Moderate')
        timeline = request.form.get('timeline', 'Standard (3-6 months)')
        leadership = request.form.get('leadership', 'Cross-functional team')
        
        # Read and parse files
        readiness_content = readiness_file.read().decode('utf-8')
        toolbox_content = toolbox_file.read().decode('utf-8')
        
        readiness_data = parse_text_file(readiness_content, 'readiness')
        toolbox_data = parse_text_file(toolbox_content, 'toolbox')
        
        # Create session data
        session_data = {
            'companyName': company_name,
            'readiness': readiness_data,
            'toolbox': toolbox_data,
            'strategic': {
                'primaryDriver': primary_driver,
                'riskTolerance': risk_tolerance,
                'timeline': timeline,
                'leadership': leadership
            }
        }
        
        # Generate playbook
        pdf_path = generate_complete_playbook_branded(session_data, BASE_PDF_PATH)
        
        # Return the PDF
        return send_file(
            pdf_path,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=f'{company_name.replace(" ", "_")}_AI_Playbook.pdf'
        )
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/test-generate', methods=['GET'])
def test_generate():
    """Test endpoint with sample data"""
    try:
        # Use the uploaded test files
        with open('/home/ubuntu/upload/ai-readiness-report-2025-10-20.txt', 'r') as f:
            readiness_data = parse_text_file(f.read(), 'readiness')
        
        with open('/home/ubuntu/upload/MESH-AI-Recommendations-2025-10-20.txt', 'r') as f:
            toolbox_data = parse_text_file(f.read(), 'toolbox')
        
        session_data = {
            'companyName': 'Test Company',
            'readiness': readiness_data,
            'toolbox': toolbox_data,
            'strategic': {
                'primaryDriver': 'Improve customer experience',
                'riskTolerance': 'Moderate',
                'timeline': 'Standard (3-6 months)',
                'leadership': 'Cross-functional team'
            }
        }
        
        pdf_path = generate_complete_playbook_branded(session_data, BASE_PDF_PATH)
        
        return send_file(
            pdf_path,
            mimetype='application/pdf',
            as_attachment=True,
            download_name='Test_Company_AI_Playbook.pdf'
        )
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("="*60)
    print("MESH AI Playbook Generator - Branded Version")
    print("="*60)
    print(f"Base PDF: {BASE_PDF_PATH}")
    print(f"Output Directory: {OUTPUT_DIR}")
    print("Starting server on http://0.0.0.0:5000")
    print("="*60)
    app.run(host='0.0.0.0', port=5000, debug=True)

