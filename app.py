from flask import Flask, request, jsonify, send_file
import sbol3
from sbol_utilities import component
from sbol_utilities.component import ed_restriction_enzyme, backbone, part_in_backbone,  part_in_backbone_from_sbol, \
    digestion, ligation, Assembly_plan_composite_in_backbone_single_enzyme, backbone_from_sbol
from sbol_utilities.conversion import convert_from_genbank, convert3to2
from Bio import Restriction
import os




app = Flask(__name__)

@app.route("/", methods=['POST', 'GET'])
async def getSBOL():
    SBOL_data = {}

    # Convert DAMP Lab Canvas Parameters to SBOL 
    try:
        doc = sbol3.Document()
        sbol3.set_namespace('http://sbolstandard.org/testfiles')
        request_data = request.get_json() 
        
        # Vector and Insert and sequences
        vector_data = request_data['Vector']
        insert_data = request_data['Insert']

        # The data will be Enzyme name
        first_restriction_site_data = request_data['First Restriction Site']
        second_restriction_site_data = request_data['Second Restriction Site']

        create_vector(doc, vector_data)
        create_insert(doc, insert_data)
        # create_first_restriction_site(doc, first_restriction_site_data)
        # create_second_restriction_site(doc, second_restriction_site_data)
        doc.write("test.xml")
        
        if SBOL_data is None:
            raise ValueError("No JSON received")

    except Exception as e:
        # Handle missing fields or errors with a fallback response
        SBOL_data = {
            "Error": str(e)
        }

        
    sbol_data = await send_file("test.xml", 
                     mimetype='application/xml', 
                     as_attachment=True, 
                     download_name='output.xml') 
        
    return sbol_data

def create_vector(doc, sequence):
    vector = sbol3.Component("Vector", sbol3.SBO_DNA)
    doc.add(vector)
    vector_sequence = sbol3.Sequence("vectorSequence", elements=sequence, encoding=sbol3.IUPAC_DNA_ENCODING)
    doc.add(vector_sequence)

def create_insert(doc, sequence):
    insert = sbol3.Component("Insert", sbol3.SBO_DNA)
    doc.add(insert)
    insert_sequence = sbol3.Sequence("insert_sequence", elements=sequence, encoding=sbol3.IUPAC_DNA_ENCODING)
    doc.add(insert_sequence)

def create_first_restriction_site(doc, enzyme_name):
    all_enzymes = Restriction.AllEnzymes
    for enzyme in all_enzymes:
        if enzyme.__name__ == enzyme_name:
            print(f"Name: {enzyme_name}, URI: {enzyme.uri}")
        
    enzyme_type = "SBO_0000014"

    first_restriction_site_enzyme = sbol3.Component("first_restriction_enzyme", enzyme_type, type_uri=enzyme.uri)
    doc.add(first_restriction_site_enzyme)

    enzyme_sequence = sbol3.Sequence("first_restriction_site_enzyme", elements="TEST", encoding=sbol3.IUPAC_DNA_ENCODING)
    doc.add(enzyme_sequence)

def create_second_restriction_site(doc, enzyme_name):
    all_enzymes = Restriction.AllEnzymes
    for enzyme in all_enzymes:
        if enzyme.__name__ == enzyme_name:
            print(f"Name: {enzyme_name}, URI: {enzyme.uri}")
        

    # enzyme = ed_restriction_enzyme(enzyme_name)
    # doc.add(enzyme)

    enzyme_type = "SBO_0000014"

    second_restriction_site_enzyme = sbol3.Component("second_restriction_enzyme", enzyme_type, type_uri=enzyme.uri)
    doc.add(second_restriction_site_enzyme)

    enzyme_sequence = sbol3.Sequence("second_restriction_site_enzyme", elements="TEST", encoding=sbol3.IUPAC_DNA_ENCODING)
    doc.add(enzyme_sequence)

        


if __name__ == '__main__':
  app.run(debug=True)
