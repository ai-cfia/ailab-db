DROP FUNCTION IF EXISTS extract_seed_info_by_common_name(text);

-- Create a PL/pgSQL function to extract seed information by common name
CREATE OR REPLACE FUNCTION extract_seed_info_by_common_name(
    seed_common_name text
) RETURNS TABLE (
    common_name text,
    family text,
    regulation text,
    life_cycle text,
    seed_or_fruit_type text,
    seed_length text,
    seed_width text,
    shape text,
    surface_texture text,
    colour text,
    other_features text,
    habitat_and_crop_association text,
    photos text[]  
) AS $$
BEGIN
    RETURN QUERY
    SELECT
        -- Common Name (with HTML tags removed)
        REGEXP_REPLACE(
            SUBSTRING(content, POSITION('<h2>Common Name</h2>' IN content) + LENGTH('<h2>Common Name</h2>'),
                      POSITION('</p>' IN SUBSTRING(content, POSITION('<h2>Common Name</h2>' IN content) + LENGTH('<h2>Common Name</h2>'), 1000)) - 1),
            '<[^>]+>',
            '',
            'g'
        ) AS common_name,
        -- Family (with HTML tags removed)
        REGEXP_REPLACE(
            SUBSTRING(content, POSITION('<h2>Family</h2>' IN content) + LENGTH('<h2>Family</h2>'),
                      POSITION('</p>' IN SUBSTRING(content, POSITION('<h2>Family</h2>' IN content) + LENGTH('<h2>Family</h2>'), 1000)) - 1),
            '<[^>]+>',
            '',
            'g'
        ) AS family,
        -- Regulation (with HTML tags removed)
        REGEXP_REPLACE(
            SUBSTRING(content, POSITION('<h2>Regulation</h2>' IN content) + LENGTH('<h2>Regulation</h2>'),
                      POSITION('</p>' IN SUBSTRING(content, POSITION('<h2>Regulation</h2>' IN content) + LENGTH('<h2>Regulation</h2>'), 1000)) - 1),
            '<[^>]+>',
            '',
            'g'
        ) AS regulation,
        -- Duration of life cycle (with HTML tags removed)
        REGEXP_REPLACE(
            SUBSTRING(content, POSITION('<h2>Duration of life cycle</h2>' IN content) + LENGTH('<h2>Duration of life cycle</h2>'),
                      POSITION('</p>' IN SUBSTRING(content, POSITION('<h2>Duration of life cycle</h2>' IN content) + LENGTH('<h2>Duration of life cycle</h2>'), 1000)) - 1),
            '<[^>]+>',
            '',
            'g'
        ) AS life_cycle,
        -- Seed or fruit type (with HTML tags removed)
        REGEXP_REPLACE(
            SUBSTRING(content, POSITION('<h2>Seed or fruit type</h2>' IN content) + LENGTH('<h2>Seed or fruit type</h2>'),
                      POSITION('</p>' IN SUBSTRING(content, POSITION('<h2>Seed or fruit type</h2>' IN content) + LENGTH('<h2>Seed or fruit type</h2>'), 1000)) - 1),
            '<[^>]+>',
            '',
            'g'
        ) AS seed_or_fruit_type,
        -- Seed length (with HTML tags removed)
		REGEXP_REPLACE(
		    SUBSTRING(content, POSITION('<li>Seed length:' IN content) + LENGTH('<li>Seed length:'),
		              POSITION('</abbr></li>' IN SUBSTRING(content, POSITION('<li>Seed length:' IN content) + LENGTH('<li>Seed length:'), 1000)) - 1),
		    '<[^>]+>',
		    '',
		    'g'
		) AS seed_length,
        -- Seed width (with HTML tags removed)
		REGEXP_REPLACE(
		    SUBSTRING(content, POSITION('<li>Seed width:' IN content) + LENGTH('<li>Seed width:'),
		              POSITION('</abbr></li>' IN SUBSTRING(content, POSITION('<li>Seed width:' IN content) + LENGTH('<li>Seed width:'), 1000)) - 1),
		    '<[^>]+>',
		    '',
		    'g'
		) AS seed_width,
        -- Shape (with HTML tags removed)
        REGEXP_REPLACE(
            SUBSTRING(content, POSITION('<h3 class="mrgn-lft-lg">Shape</h3>' IN content) + LENGTH('<h3 class="mrgn-lft-lg">Shape</h3>'),
                    POSITION('</li>' IN SUBSTRING(content, POSITION('<h3 class="mrgn-lft-lg">Shape</h3>' IN content) + LENGTH('<h3 class="mrgn-lft-lg">Shape</h3>'), 1000)) - 1),
            '<[^>]+>',
            '',
            'g'
        ) AS shape,
        -- Surface Texture (with HTML tags removed)
        REGEXP_REPLACE(
            SUBSTRING(content, POSITION('<h3 class="mrgn-lft-lg">Surface Texture</h3>' IN content) + LENGTH('<h3 class="mrgn-lft-lg">Surface Texture</h3>'),
                    POSITION('</li>' IN SUBSTRING(content, POSITION('<h3 class="mrgn-lft-lg">Surface Texture</h3>' IN content) + LENGTH('<h3 class="mrgn-lft-lg">Surface Texture</h3>'), 1000)) - 1),
            '<[^>]+>',
            '',
            'g'
        ) AS surface_texture,
        -- Colour (with HTML tags removed)
        REGEXP_REPLACE(
            SUBSTRING(content, POSITION('<h3 class="mrgn-lft-lg">Colour</h3>' IN content) + LENGTH('<h3 class="mrgn-lft-lg">Colour</h3>'),
                    POSITION('</li>' IN SUBSTRING(content, POSITION('<h3 class="mrgn-lft-lg">Colour</h3>' IN content) + LENGTH('<h3 class="mrgn-lft-lg">Colour</h3>'), 1000)) - 1),
            '<[^>]+>',
            '',
            'g'
        ) AS colour,
        -- Other Features (with HTML tags removed)
        REGEXP_REPLACE(
            SUBSTRING(content, POSITION('<h3 class="mrgn-lft-lg">Other Features</h3>' IN content) + LENGTH('<h3 class="mrgn-lft-lg">Other Features</h3>'),
                    POSITION('</li>' IN SUBSTRING(content, POSITION('<h3 class="mrgn-lft-lg">Other Features</h3>' IN content) + LENGTH('<h3 class="mrgn-lft-lg">Other Features</h3>'), 1000)) - 1),
            '<[^>]+>',
            '',
            'g'
        ) AS other_features,
        -- Habitat and Crop Association (with HTML tags removed)
        REGEXP_REPLACE(
            SUBSTRING(content, POSITION('<h2>Habitat and Crop Association</h2>' IN content) + LENGTH('<h2>Habitat and Crop Association</h2>'),
                    POSITION('</p>' IN SUBSTRING(content, POSITION('<h2>Habitat and Crop Association</h2>' IN content) + LENGTH('<h2>Habitat and Crop Association</h2>'), 1000)) - 1),
            '<[^>]+>',
            '',
            'g'
        ) AS habitat_and_crop_association,
		ARRAY(  
		    SELECT (REGEXP_MATCHES(sub_content, '<img alt="" class="img-responsive" src="([^"]+)"', 'g'))[1]  
		    FROM (  
		        SELECT SPLIT_PART(content, '<h3>Similar species</h3>', 1) AS sub_content  
		        FROM html_content  
		        WHERE content LIKE ('%<h2>Common Name</h2>%' || seed_common_name || '%')  
		    ) AS subquery  
		) AS photos  
FROM  
    html_content hc  -- Replace with the actual table name containing the HTML content  
WHERE  
    content LIKE ('%<h2>Common Name</h2>%' || seed_common_name || '%');  
END;  
$$ LANGUAGE plpgsql; 

SELECT * FROM extract_seed_info_by_common_name('Velvetleaf');

CREATE OR REPLACE FUNCTION extract_seed_info_as_json(    
    seed_common_name text    
) RETURNS json AS $$    
DECLARE    
    seed_info_record RECORD;    
BEGIN    
    -- Call the existing function to get the data    
    SELECT * INTO seed_info_record FROM extract_seed_info_by_common_name(seed_common_name);    
        
    -- Construct a JSON object with the retrieved data using field names    
    RETURN json_build_object(    
        'family', trim(seed_info_record.family),    
        'common_name', trim(seed_info_record.common_name),    
        'duration_of_life_cycle', trim(seed_info_record.life_cycle),    
        'seed_or_fruit_type', trim(seed_info_record.seed_or_fruit_type),    
        'identification_features', json_build_object(    
            'seed_length', trim(seed_info_record.seed_length),    
            'seed_width', trim(seed_info_record.seed_width),    
            'shape', trim(seed_info_record.shape),    
            'surface_texture', trim(seed_info_record.surface_texture),    
            'colour', trim(seed_info_record.colour),    
            'other_features', trim(seed_info_record.other_features)    
        ),    
        'images', seed_info_record.photos,    
        'source', 'https://inspection.canada.ca/plant-health/seeds/seed-testing-and-grading/seeds-identification/abutilon-theophrasti/eng/1472604373914/1472604374428'    
    );    
END;    
$$ LANGUAGE plpgsql;   

-- Utilisez la nouvelle fonction pour extraire et renvoyer les données au format JSON
SELECT extract_seed_info_as_json('Velvetleaf');
