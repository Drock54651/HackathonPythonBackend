from flask import Flask, request, jsonify
import sbol3
from sbol_utilities import component
from sbol_utilities.component import ed_restriction_enzyme, backbone, part_in_backbone,  part_in_backbone_from_sbol, \
    digestion, ligation, Assembly_plan_composite_in_backbone_single_enzyme, backbone_from_sbol
from sbol_utilities.conversion import convert_from_genbank, convert3to2


app = Flask(__name__)

@app.route("/", methods=['POST', 'GET'])
def getSBOL():
    SBOL_data = {}

    # Convert DAMP Lab Canvas Parameters to SBOL 
    try:
        doc = sbol3.Document()
        sbol3.set_namespace('http://sbolstandard.org/testfiles')
        request_data = request.get_json() 
        
        # Vector and Insert and sequences
        SBOL_data["Vector"] = request_data['Vector']
        SBOL_data["Insert"] = request_data['Insert']
        SBOL_data["First Restriction Site"] = request_data['First Restriction Site']
        SBOL_data["Second Restriction Site"] = request_data['Second Restriction Site']
        vector = sbol3.Component("Vector", sbol3.SBO_DNA)
        doc.add(vector)
        vector_sequence = sbol3.Sequence("vectorSequence", elements=SBOL_data["Vector"],)
        


        
        if SBOL_data is None:
            raise ValueError("No JSON received")

    except Exception as e:
        # Handle missing fields or errors with a fallback response
        SBOL_data = {
            "Error": str(e)
        }

    return jsonify(SBOL_data)  # Flask will convert this to JSON



if __name__ == '__main__':
  app.run(debug=True)
