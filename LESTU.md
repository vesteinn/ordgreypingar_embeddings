# Greypingar ([English](https://github.com/stofnun-arna-magnussonar/ordgreypingar_embeddings/blob/main/README.md))
Þetta varðveislusafn hýsir gagnasöfn sem meta getu orðvigralíkana til þess að átta sig á merkingarfræði og orðhlutafræði íslensku, auk forþjálfaðra greypinga sem hafa verið metnar með téðum gagnasöfnum.

Nánar tiltekið geta notendur vefsins beitt efni hans til að framkvæma eitt eða fleiri af eftirfarandi verkum:

1. Tilreiða þær inntaksskrár sem nauðsynlegar eru til að þjálfa greypingar.
2. Þjálfa greypingar með word2vec, fastText, og/eða GloVe aðferðafræðinni.
3. Leggja mat á gæði greypinganna með öðru hvoru gagnasafnanna: MSL eða IceBATS.

Vinsamlegast athugaðu að þjálfun og mat greypinganna krefjast þess gjarnan að viðkomandi tölvubúnaður búi yfir ríflegu magni af minni (og, þegar GloVe er beitt, nægu geymsluplássi), og geta tekið þó nokkurn tíma. Ef þú ert einungis að prufukeyra forritskóðann gætirðu viljað útbúa smærri inntaksskrár frekar en að beita Risamálheildinni (RMH) í fullri stærð og stilla tímabilsbreytur („epoch“) á lág gildi til að takmarka keyrslutíma. Ætlirðu einungis að beita gagnasöfnum til þess að meta forþjálfaðar greypingar og þarft þar af leiðandi ekki að þjálfa greypingar frá grunni mælum við með að fylgja því fordæmi í forritskóðanum að nota einungis vigraskrár til slíks, frekar en líkanaskrárnar í heild sinni.

# Tilreiðing inntaksskráa

Gögnin sem við notum eru fengin úr Risamálheildinni (RMH) sem eru aðgengileg í gegnum [CLARIN](https://clarin.is/en/resources/gigaword/) eða á [vef Árnastofnunar](http://igc.arnastofnun.is/is/index.html). Í forritskóða þessa safns er gert ráð fyrir að RMH gögn séu aðgengileg í /RMH/ undirmöppu.

Tilreiðingarkóðinn er aðgengilegur í [/prep_code_general/](https://github.com/stofnun-arna-magnussonar/ordgreypingar_embeddings/tree/main/prep_code_general) möppunni. Nota skal annað hvort get_lemmatized_sents.py til að smíða inntaksskrá úr lemmuðum gögnum RMH, eða get_original_sents.py til að smíða inntaksskrá án þess að lemma fyrst gögnin.

Ætlirðu að nota GloVe til að þjálfa greypingar muntu einnig þurfa að keyra make_oneline.py á inntaksskrána.

# Þjálfun greypinga

Forritskóða fyrir hverja þjálfunaraðferð má finna í samnefndum möppum. Athugaðu að kóðinn mun ekki einungis þjálfa greypingar, heldur mun hann einnig meta þær í beinu framhaldi. Stutt lýsing á því hvernig megi sleppa matsferlinu fylgir hér að neðan.

Forritskóðinn gerir almennt ráð fyrir því að inntaksskrá, auk gagnaskráa fyrir matsferlið, sé staðsett í sömu möppu og Python forritið sem keyrt er. Hver mappa inniheldur einnig test_analogies.py skrá sem inniheldur nauðsynlega virkni fyrir matshlutann. Ætlirðu einungis að þjálfa greypingar og ekki meta þær geturðu fjarlægt þann forritskóða sem kallar á föll úr þessari skrá.

Til að þjálfa [word2vec](https://github.com/stofnun-arna-magnussonar/ordgreypingar_embeddings/tree/main/word2vec) og [fastText](https://github.com/stofnun-arna-magnussonar/ordgreypingar_embeddings/tree/main/fastText) þarftu einfaldlega að keyra train_w2v.py eða gsft.py skrárnar. Þær eru eins uppsettar. Ef þú vilt sleppa ferlinu þar sem gæði greypinganna eru metin þarftu að útiloka allt train_model() fallið sem kemur á eftir mod_vectors.save() fallinu.

[GloVe](https://github.com/stofnun-arna-magnussonar/ordgreypingar_embeddings/tree/main/GloVe) er hins vegar ekki hægt að keyra beint gegnum Python forrit. Þess í stað þarf að keyra glove_train.sh Bash skriptu sem kallar svo sjálfvirkt á Python kóðann. Í raun og veru er sjálf þjálfunin einskorðuð við Bash skriptuna en Python forritið er einungis nýtt í matshlutanum. Viljirðu einungis þjálfa greypingar og ekki meta þær geturðu opnað glove_train.sh skriptuna og ógildað þær tvær línur neðst í skjalinu sem innihalda tilvísanir í glove_msl.py.

# Mat á greypingum
Eins og kom fram hér að ofan er forritskóðinn sem metur word2vec og fastText staðsettur í seinni helmingi train_model() fallanna í samsvarandi Python skrám fyrir þessar aðferðir, beint á eftir kallinu á mod_vectors.save() fallið.

Hvað varðar GloVe er það hins vegar Bash skriptan sem framkvæmir þjálfunina og kallar svo rétt undir lokin á Python skrá til að keyra sjálft matið. Til að einskorða þig við matsferlið þarftu því annað hvort að ógilda obbann af kóðanum í Bash skriptunni eða einfaldlega keyra Python skrána beint á sama hátt og gert er í síðustu línunni (þeirri sem inniheldur tilvísun í glove_msl.py) í skriptunni.

Tvær ólíkar matsaðferðir standa til boða: [MSL](https://github.com/stofnun-arna-magnussonar/ordgreypingar_embeddings/tree/main/MSL), sem er byggt á Multi-Simlex, og [IceBATS](https://github.com/stofnun-arna-magnussonar/ordgreypingar_embeddings/tree/main/IceBATS), sem er byggt á The Bigger Analogy Test Set. Hvor aðferðin fyrir sig inniheldur auk þess nokkur ólík skref. Þegar verið er að meta líkön er ekki skilyrði að beita báðum aðferðum og óhætt er að ógilda þær forritslínur sem myndu kalla á þá aðferð sem ekki er þörf á. Strangt til tekið er heldur ekki nauðsynlegt að keyra hvert einasta skref innan hvorrar aðferðar en hafa ber í huga að séu einhverjir kostir útilokaðir munu matsniðurstöður ekki lengur vera sambærilegar við fyrri keyrslur MSL eða BATS. Ítarlegar lýsingar á hverju skrefi fyrir sig má finna í viðeigandi fræðigreinum um upprunalegar útfærslur MSL og BATS gagnasafnanna.

Eins áður hefur verið minnst á getur matsferlið, rétt eins og þjálfunarferlið, verið frekar krefjandi á þann vélbúnað sem notast er við, sérstaklega hvað varðar innra minni tölvu. Við höfum reynt að minnka þetta álag meðal annars með því að lágmarka fjölda af forritsbreytum sem hýsa orðvigralíkönin í heild sinni. Komi það reglulega til hjá þér að forritið ljúki ekki keyrslu - til dæmis ef keyrsla þess er stöðvuð af eigin stýrikerfi - eða ef úttaksskrár þess reynast vera tómar þrátt fyrir að keyrsla virðist ljúka eðlilega, gætirðu viljað keyra prófanir með greypingum sem byggðar eru á smærri inntaksskrám frekar en RMH í fullri stærð eða prófanir sem einungis nota sum skrefin sem eru í boði.
