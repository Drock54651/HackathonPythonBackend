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
        vector_data = request_data['Vector']
        insert_data = request_data['Insert']
        first_restriction_site_data = request_data['First Restriction Site']
        second_restriction_site_data = request_data['Second Restriction Site']

        create_vector(doc, vector_data)
        create_insert(doc, insert_data)
        create_first_restriction_site(doc, first_restriction_site_data)
        create_second_restriction_site(doc, second_restriction_site_data)
        
        if SBOL_data is None:
            raise ValueError("No JSON received")

    except Exception as e:
        # Handle missing fields or errors with a fallback response
        SBOL_data = {
            "Error": str(e)
        }

    return jsonify(SBOL_data)  # Flask will convert this to JSON

def create_vector(doc, data):
    vector = sbol3.Component("Vector", sbol3.SBO_DNA)
    doc.add(vector)
    vector_sequence = sbol3.Sequence("vectorSequence", elements=data, encoding=sbol3.Sequence.IUPAC_DNA_ENCODING)
    doc.add(vector_sequence)

def create_insert(doc, data):
    insert = sbol3.Component("Insert", sbol3.SBO_DNA)
    doc.add(insert)
    insert_sequence = sbol3.Sequence("insert_sequence", elements=data, encoding=sbol3.Sequence.IUPAC_DNA_ENCODING)
    doc.add(insert_sequence)

def create_first_restriction_site(doc, data):
    first_restriction_site_enzyme = sbol3.Component("first_restriction_enzyme", sbol3.SBO_BIOCHEMICAL_REACTION)
    doc.add(first_restriction_site_enzyme)
    enzyme_sequence = sbol3.Sequence("first_restriction_site_enzyme", elements=data, encoding=sbol3.Sequence.IUPAC_DNA_ENCODING)
    doc.add(enzyme_sequence)

def create_second_restriction_site(doc, data):
    second_restriction_site_enzyme = sbol3.Component("second_restriction_enzyme", sbol3.SBO_BIOCHEMICAL_REACTION)
    doc.add(second_restriction_site_enzyme)
    enzyme_sequence = sbol3.Sequence("second_restriction_site_enzyme", elements=data, encoding=sbol3.Sequence.IUPAC_DNA_ENCODING)
    doc.add(enzyme_sequence)

        


if __name__ == '__main__':
  app.run(debug=True)