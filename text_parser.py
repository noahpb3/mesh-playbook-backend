import re
import json

def parse_readiness_assessment(content):
    """Parse the AI Readiness Assessment report format"""
    data = {
        'overallScore': 0,
        'maturityLevel': 'Exploring',
        'maturityDescription': '',
        'dimensionScores': {
            'strategyVision': 0,
            'dataSystems': 0,
            'peopleSkills': 0,
            'governanceEthics': 0,
            'executionImpact': 0
        },
        'dimensionDetails': {},
        'recommendations': {
            'high': [],
            'medium': []
        }
    }
    
    # Extract overall score
    overall_match = re.search(r'Overall AI Readiness Score:\s*(\d+)', content, re.IGNORECASE)
    if overall_match:
        data['overallScore'] = int(overall_match.group(1))
    
    # Extract maturity level
    maturity_match = re.search(r'Maturity Level:\s*([^\n]+)', content, re.IGNORECASE)
    if maturity_match:
        data['maturityLevel'] = maturity_match.group(1).strip()
    
    # Extract maturity description
    desc_match = re.search(r'Description:\s*([^\n]+)', content, re.IGNORECASE)
    if desc_match:
        data['maturityDescription'] = desc_match.group(1).strip()
    
    # Extract dimension scores with emojis and descriptions
    dimension_patterns = {
        'strategyVision': r'(?:🧭\s*)?Strategy\s*&\s*Vision[^\n]*\n\s*Score:\s*(\d+)',
        'dataSystems': r'(?:💾\s*)?Data\s*&\s*Systems[^\n]*\n\s*Score:\s*(\d+)',
        'peopleSkills': r'(?:👥\s*)?People\s*&\s*Skills[^\n]*\n\s*Score:\s*(\d+)',
        'governanceEthics': r'(?:🛡️\s*)?Governance\s*&\s*Ethics[^\n]*\n\s*Score:\s*(\d+)',
        'executionImpact': r'(?:🚀\s*)?Execution\s*&\s*Impact[^\n]*\n\s*Score:\s*(\d+)'
    }
    
    for dim_key, pattern in dimension_patterns.items():
        match = re.search(pattern, content, re.IGNORECASE)
        if match:
            data['dimensionScores'][dim_key] = int(match.group(1))
            
            # Extract description for this dimension
            desc_pattern = pattern + r'[^\n]*\n([^\n]+)'
            desc_match = re.search(desc_pattern, content, re.IGNORECASE)
            if desc_match:
                data['dimensionDetails'][dim_key] = desc_match.group(2).strip()
    
    # Extract HIGH PRIORITY recommendations
    high_section = re.search(r'HIGH PRIORITY\s*-+\s*(.+?)(?:MEDIUM PRIORITY|={3,}|$)', content, re.DOTALL | re.IGNORECASE)
    if high_section:
        recommendations = parse_recommendations_section(high_section.group(1))
        data['recommendations']['high'] = recommendations
    
    # Extract MEDIUM PRIORITY recommendations
    medium_section = re.search(r'MEDIUM PRIORITY\s*-+\s*(.+?)(?:={3,}|$)', content, re.DOTALL | re.IGNORECASE)
    if medium_section:
        recommendations = parse_recommendations_section(medium_section.group(1))
        data['recommendations']['medium'] = recommendations
    
    return data

def parse_recommendations_section(section_text):
    """Parse individual recommendations with action items"""
    recommendations = []
    
    # Split by numbered recommendations
    rec_blocks = re.split(r'\n\s*\d+\.\s+', section_text)
    
    for block in rec_blocks[1:]:  # Skip first empty element
        rec = {}
        lines = block.strip().split('\n')
        
        if lines:
            # First line is the title
            title_match = re.match(r'(.+?)\s*\(([^)]+)\)', lines[0])
            if title_match:
                rec['title'] = title_match.group(1).strip()
                rec['dimension'] = title_match.group(2).strip()
            else:
                rec['title'] = lines[0].strip()
                rec['dimension'] = ''
            
            # Extract description (text before "Action Items:")
            desc_lines = []
            action_items = []
            in_actions = False
            
            for line in lines[1:]:
                line = line.strip()
                if 'Action Items:' in line:
                    in_actions = True
                    continue
                
                if in_actions:
                    # Extract numbered action items
                    action_match = re.match(r'\d+\.\s*(.+)', line)
                    if action_match:
                        action_items.append(action_match.group(1).strip())
                else:
                    if line:
                        desc_lines.append(line)
            
            rec['description'] = ' '.join(desc_lines)
            rec['actionItems'] = action_items
            
            if rec.get('title'):
                recommendations.append(rec)
    
    return recommendations

def parse_toolbox_recommendations(content):
    """Parse the MESH AI Toolbox Recommendations format"""
    data = {
        'readinessScore': 0,
        'industry': '',
        'companySize': '',
        'budgetRange': '',
        'implementationGuidance': '',
        'recommendedTools': [],
        'nextSteps': []
    }
    
    # Extract profile information
    profile_match = re.search(r'AI Readiness Score:\s*(\d+)', content)
    if profile_match:
        data['readinessScore'] = int(profile_match.group(1))
    
    industry_match = re.search(r'Industry:\s*([^\n]+)', content, re.IGNORECASE)
    if industry_match:
        data['industry'] = industry_match.group(1).strip()
    
    size_match = re.search(r'Company Size:\s*([^\n]+)', content, re.IGNORECASE)
    if size_match:
        data['companySize'] = size_match.group(1).strip()
    
    budget_match = re.search(r'Budget:\s*([^\n$]+)', content, re.IGNORECASE)
    if budget_match:
        data['budgetRange'] = budget_match.group(1).strip()
    
    # Extract implementation guidance
    guidance_match = re.search(r'IMPLEMENTATION GUIDANCE\s*(.+?)(?:={3,})', content, re.DOTALL | re.IGNORECASE)
    if guidance_match:
        data['implementationGuidance'] = guidance_match.group(1).strip()
    
    # Extract recommended tools
    tools_section = re.search(r'RECOMMENDED TOOLS.*?\n\s*(.+?)(?:={3,}|BUDGET PLANNING|NEXT STEPS)', content, re.DOTALL | re.IGNORECASE)
    if tools_section:
        tools_text = tools_section.group(1)
        
        # Split by numbered tools - use lookahead to keep the number
        tool_blocks = re.split(r'\n(?=\d+\.\s+)', tools_text)
        
        for block in tool_blocks:
            block = block.strip()
            if block and re.match(r'\d+\.\s+', block):
                # Remove the number prefix
                block = re.sub(r'^\d+\.\s+', '', block)
                tool = parse_tool_block(block)
                if tool:
                    data['recommendedTools'].append(tool)
    
    # Extract next steps
    next_steps_match = re.search(r'NEXT STEPS\s*(.+?)(?:={3,}|$)', content, re.DOTALL | re.IGNORECASE)
    if next_steps_match:
        steps_text = next_steps_match.group(1).strip()
        steps = re.findall(r'\d+\.\s*([^\n]+)', steps_text)
        data['nextSteps'] = [step.strip() for step in steps]
    
    return data

def parse_tool_block(block):
    """Parse individual tool recommendation block"""
    tool = {
        'name': '',
        'priority': '',
        'matchScore': 0,
        'category': '',
        'website': '',
        'whyRecommend': [],
        'keyFeatures': [],
        'pricing': []
    }
    
    lines = block.strip().split('\n')
    if not lines:
        return None
    
    # First line: Tool name and priority
    first_line = lines[0].strip()
    name_match = re.match(r'(.+?)\s*\[([^\]]+)\]', first_line)
    if name_match:
        tool['name'] = name_match.group(1).strip()
        tool['priority'] = name_match.group(2).strip()
    else:
        tool['name'] = first_line
    
    current_section = None
    
    for line in lines[1:]:
        line = line.strip()
        
        # Check for section headers
        if line.startswith('Match Score:'):
            match = re.search(r'(\d+)', line)
            if match:
                tool['matchScore'] = int(match.group(1))
        elif line.startswith('Category:'):
            tool['category'] = line.replace('Category:', '').strip()
        elif line.startswith('Website:'):
            tool['website'] = line.replace('Website:', '').strip()
        elif line.startswith('Why We Recommend:'):
            current_section = 'why'
        elif line.startswith('Key Features:'):
            current_section = 'features'
        elif line.startswith('Pricing:'):
            current_section = 'pricing'
        elif line.startswith('•'):
            # Bullet point
            item = line.replace('•', '').strip()
            if current_section == 'why':
                tool['whyRecommend'].append(item)
            elif current_section == 'features':
                tool['keyFeatures'].append(item)
            elif current_section == 'pricing':
                tool['pricing'].append(item)
        elif line and current_section == 'pricing' and ':' in line:
            # Pricing tier
            tool['pricing'].append(line)
    
    return tool if tool['name'] else None

def parse_text_file(content, file_type='auto'):
    """Main parser function that routes to appropriate parser"""
    
    # Try to detect file type if auto
    if file_type == 'auto':
        if 'AI READINESS ASSESSMENT' in content.upper():
            file_type = 'readiness'
        elif 'MESH AI TOOLBOX' in content.upper() or 'RECOMMENDED TOOLS' in content.upper():
            file_type = 'toolbox'
        else:
            # Fallback: try both and see which gives better results
            if 'Overall AI Readiness Score' in content or 'Maturity Level' in content:
                file_type = 'readiness'
            else:
                file_type = 'toolbox'
    
    if file_type == 'readiness':
        return parse_readiness_assessment(content)
    elif file_type == 'toolbox':
        return parse_toolbox_recommendations(content)
    else:
        return {}

