//NanoMine tools script for mongo

//listSchemas()
function listSchemas() {
  db = db.getSiblingDB('mgi');
  db.template
    .find()
    .forEach(function(doc) {
         print(doc.title+' '+doc._id);
       });
}
// listXmlsForSchema(schemaId) 
function listXmlsForSchema(schemaId) {
  db = db.getSiblingDB('mgi');
  db.xmldata
    .find({'schema':{ $eq: schemaId}})
    .forEach(function(doc) {
      print(doc.schema + ' ' + doc._id+ ' ' + doc.title);
    });
}

