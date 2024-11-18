from flask import Flask, request, jsonify, send_file
import sbol3
from sbol_utilities import component
from sbol_utilities.component import ed_restriction_enzyme, backbone, part_in_backbone,  part_in_backbone_from_sbol, \
    digestion, ligation, Assembly_plan_composite_in_backbone_single_enzyme, backbone_from_sbol
from sbol_utilities.conversion import convert_from_genbank, convert3to2
from Bio import Restriction


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

        # The data will be Enzyme name
        first_restriction_site_data = request_data['First Restriction Site'] #SapI
        second_restriction_site_data = request_data['Second Restriction Site'] #BsaI

        create_vector(doc, vector_data)
        create_insert(doc, insert_data)
        part = attach_backbone(doc, insert_data, first_restriction_site_data, True)
        part2 = attach_backbone(doc, "tagc", second_restriction_site_data, True)

        part_arr = [part, part2]

        enzyme = ed_restriction_enzyme(first_restriction_site_data)

        assembly_plan = create_assembly_plan(doc, part_arr, vector_data, enzyme)
        assembly_plan.document.write("test2.xml")
        
        if SBOL_data is None:
            raise ValueError("No JSON received")

    except Exception as e:
        # Handle missing fields or errors with a fallback response
        print(e)
        

        
    sbol_data = send_file("test2.xml", 
                     mimetype='application/xml', 
                     as_attachment=True, 
                     download_name='output.xml') 
        
    return sbol_data

def create_vector(doc, sequence):
    vector = sbol3.Component("Vector_Plasmid", sbol3.SBO_DNA)
    doc.add(vector)
    vector_sequence = sbol3.Sequence("vectorSequence", elements=sequence, encoding=sbol3.IUPAC_DNA_ENCODING)
    doc.add(vector_sequence)

def create_insert(doc, sequence):
    insert = sbol3.Component("Insert", sbol3.SBO_DNA)
    doc.add(insert)
    insert_sequence = sbol3.Sequence("Insert_Plasmid", elements=sequence, encoding=sbol3.IUPAC_DNA_ENCODING)
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

    second_restriction_site_enzyme = sbol3.Component("second_restriction_enzyme", enzyme_type, type_uri=enzyme.uri)
    doc.add(second_restriction_site_enzyme)

    enzyme_sequence = sbol3.Sequence("second_restriction_site_enzyme", elements="TEST", encoding=sbol3.IUPAC_DNA_ENCODING)
    doc.add(enzyme_sequence)

def attach_backbone(doc, insert_sequence, enzyme_name, is_linear):
    part_index = len(doc)+1
    fusion_site_length = 0
    enzyme_name
    
    # get fusion site length for enzyme
    for enzyme in Restriction.AllEnzymes:
        if enzyme.__name__ == enzyme_name:
            enzyme_name = enzyme
            fusion_site_length = abs(enzyme.ovhg)
    
    # turn sequence into component
    part = sbol3.Component(f'part{part_index}', sbol3.SBO_DNA, name=f'part{part_index}')
    
    doc.add(part)
    part_seq = sbol3.Sequence(f'{part.name}Sequence', elements=insert_sequence, encoding=sbol3.IUPAC_DNA_ENCODING)
    doc.add(part_seq)
    part.sequences = [ part_seq ]

    #                                                         #   name,             part obj,   part locations(in bb), role, 
    part_in_bb, part_in_bb_seq = part_in_backbone_from_sbol(f'{part.name}_in_bb', part, [1,len(insert_sequence)], [], fusion_site_length, is_linear, name=f'{part.name}_in_bb')
    doc.add([part_in_bb, part_in_bb_seq])
    
    return part_in_bb

def create_assembly_plan(doc, part_arr, vector_backbone, enzyme):    
    try:
        simple_assembly_plan = Assembly_plan_composite_in_backbone_single_enzyme(
            name='Modular_Cloning',
            parts_in_backbone=part_arr,
            acceptor_backbone=vector_backbone,
            restriction_enzyme=enzyme,
            document=doc)
            
        simple_assembly_plan.run()
    except Exception as e:
        print(e)
    return simple_assembly_plan

if __name__ == '__main__':
  app.run(debug=True)
