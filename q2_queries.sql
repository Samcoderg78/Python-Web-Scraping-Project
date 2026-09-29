-- Q2: Rfam public MySQL database
-- Connect:  mysql --user=rfamro --host=mysql-rfam-public.ebi.ac.uk --port=4497 --database=Rfam

-- 1. How many types (species) of Acacia are in the taxonomy table?
SELECT COUNT(DISTINCT species) AS acacia_species
FROM taxonomy
WHERE species LIKE 'Acacia %';

-- 2. Which type of wheat (Triticum) has the longest DNA sequence?
SELECT t.species, s.rfamseq_acc, s.length
FROM rfamseq s
JOIN taxonomy t ON t.ncbi_id = s.ncbi_id
WHERE t.species LIKE 'Triticum %'
ORDER BY s.length DESC
LIMIT 1;

-- 3 & 4. Page 9 (15 per page) of families whose longest sequence > 1,000,000
--        OFFSET = (9 - 1) * 15 = 120
SELECT f.rfam_acc       AS family_accession,
       f.rfam_id        AS family_name,
       MAX(s.length)    AS max_sequence_length
FROM family f
JOIN full_region fr ON fr.rfam_acc = f.rfam_acc
JOIN rfamseq s      ON s.rfamseq_acc = fr.rfamseq_acc
GROUP BY f.rfam_acc, f.rfam_id
HAVING MAX(s.length) > 1000000
ORDER BY max_sequence_length DESC, f.rfam_acc
LIMIT 15 OFFSET 120;
