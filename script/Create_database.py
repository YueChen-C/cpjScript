from Clib import db

Concept_stoks=('id int unsigned auto_increment','`name` nvarchar(25)','`stokcode` nvarchar(25)','`region` nvarchar(25)','`business` nvarchar(25)','`transition_type` nvarchar(25)','`industry` nvarchar(25)','`type` nvarchar(10)','PRIMARY KEY (`id`)')
db.createTable('Concept_stoks', Concept_stoks)

manage_classify=('id int unsigned auto_increment','`Nasdaq` nvarchar(10)','`shorthand` nvarchar(10)','`firstcode` nvarchar(10)','`firstname` nvarchar(10)','`towcode` nvarchar(10)','`towname` nvarchar(10)','`threecode` nvarchar(10)','`threename` nvarchar(10)','`fourcode` nvarchar(25)','`fourname` nvarchar(10)','PRIMARY KEY (`id`)')
db.createTable('manage_classify', manage_classify)

company_classify=('id int unsigned auto_increment','`Nasdaq` nvarchar(10)','`shorthand` nvarchar(10)','`firstcode` nvarchar(10)','`firstname` nvarchar(10)','`towcode` nvarchar(10)','`towname` nvarchar(10)','`threecode` nvarchar(10)','`threename` nvarchar(10)','`fourcode` nvarchar(25)','`fourname` nvarchar(10)','PRIMARY KEY (`id`)')
db.createTable('Company_classify', company_classify)