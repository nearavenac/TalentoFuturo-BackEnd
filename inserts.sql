INSERT INTO proyecto_prevencion_organismopublico (id, nombre_organismo) VALUES
(1, 'Servicio de Evaluación Ambiental'),
(2, 'Superintendencia de Electricidad y Combustibles'),
(3, 'Intendencia Regional de Valparaíso'),
(4, 'Dirección General del Territorio Marítimo y de Marina Mercante'),
(5, 'Corporación Nacional Forestal'),
(6, 'Servicio Agrícola y Ganadero'),
(7, 'Carabineros de Chile'),
(8, 'I. Municipalidades de Concón'),
(9, 'I. Municipalidades de Quintero'),
(10, 'I. Municipalidades de Puchuncaví'),
(11, 'Seremi de Salud'),
(12, 'Ministerio del Medio Ambiente'),
(13, 'Seremi del Medio Ambiente');
SELECT setval('proyecto_prevencion_organismopublico_id_seq', (SELECT MAX(id) FROM proyecto_prevencion_organismopublico));

INSERT INTO proyecto_prevencion_comunaplan (id, nombre_comuna) VALUES
(1, 'Concón'),
(2, 'Quintero'),
(3, 'Puchuncaví');
SELECT setval('proyecto_prevencion_comunaplan_id_seq', (SELECT MAX(id) FROM proyecto_prevencion_comunaplan));

INSERT INTO proyecto_prevencion_tiposmedidas (id, nombre_tipo_medida) VALUES
(1, 'Política Pública'),
(2, 'Educación y difusión'),
(3, 'Estudios');
SELECT setval('proyecto_prevencion_tiposmedidas_id_seq', (SELECT MAX(id) FROM proyecto_prevencion_tiposmedidas));

INSERT INTO proyecto_prevencion_medida (
    id,
    id_tipo_medida_id,
    nombre_corto,
    nombre_largo,
    id_organismo_id,
    regulatorio,
    descripcion_formula,
    tipo_formula,
    frecuencia
)
VALUES (
    1,
    NULL,
    'RCA que contenga obligación de compensar emisiones',  -- nombre_corto
    'Número de RCA aprobadas en el año t que contengan obligaciones de compensar emisiones atmosféricas', -- nombre_largo
    1,
    TRUE,
    'Suma del número de RCA aprobadas que contengan obligación de compensar emisiones atmosféricas',
    'Numero',
    'anual'
),
(
    2,
    NULL,
    'Condiciones del sistema de recuperación y/o eliminación de vapores de estanques Deposito techo fijo',
    'Cumplimiento de las condiciones indicadas en el literal A) para depósitos de techo fijo y Cronograma de implementación gradual calificado por la SEC cuando corresponda',
    2,
    TRUE,
    '([N° de tanques del artículo 33 literal A) al cual se han implementado las medidas comprometidas en el año t]/[N° de tanques del artículo 33 literal A) programadas para el año t]) *100',
    'Formula',
    'anual'
),
(
    3,
    NULL,
    'Requisitos del sistema de almacenamiento o intermedio',
    'Instrucciones de SEC, para cumplir con el sistema de almacenamiento intermedio u otro con el mismo objetivo, conforme al artículo 5 del DS N°160/2008.',
    2,
    TRUE,
    'Si/No',
    'Dicotomica',
    'unica'
),
(
    4,
    NULL,
    'Aprobación de sistema de almacenamient o intermedio',
    'N° de instalaciones con estanque que cuenten con un sistema de almacenamiento intermedio u otro que cumpla con el objetivo aprobado',
    2,
    TRUE,
    'Si/No',
    'Dicotomica',
    'unica'
),
(
    5,
    NULL,
    'Condiciones del sistema de recuperación y/o eliminación de vapores de estanques Deposito techo flotante',
    'Cumplimiento de las condiciones Indicadas en el literal B) para depósitos de techo flotante y Cronograma de implementación gradual calificado por la SEC, cuando corresponda',
    2,
    TRUE,
    '([N° de tanques a los cuales se les implementaron sellos primarios y/o secundarios I en el año t]/[N° de tanques programados implementar para el año t]) * 100',
    'Formula',
    'anual'
),
(
    6,
    NULL,
    'Sistema de recuperación y eliminación de vapores en fuentes emisoras de HC',
    'N° de sistemas capaz de recuperar y/o eliminar vapores que se generen en los procesos de carga y descarga, transporte, almacenamiento, distribución y abastecimiento de HC y sus derivados , en el año t',
    2,
    TRUE,
    '([N° de sistemas de recuperación y/o eliminación de vapores mantenidos con TK mayores a 200m3 ]/[N° de sistemas de recuperación y/o eliminación de vapores existentes en instalaciones con TK mayores a 200m3]) * 100',
    'Formula',
    'anual'
),
(
    7,
    NULL,
    'Almacenamien to, distribución combustibles líquidos',
    'Número de fiscalizaciones a las obligaciones del art. 177 letra g) del DS N° 160/2008 Ministerio de Economía y Fomento y Reconstrucción, en el año t',
    2,
    TRUE,
    'Suma del número de fiscalizaciones ejecutadas en el año t a instalaciones de almacenamiento y distribución de combustible',
    'Numero',
    'anual'
),
(
    8,
    NULL,
    'Sistemas de venteo dotados de piloto manual y automático',
    'N° de instalaciones con antorcha que cuenten con piloto de encendido manual y automático en el sistema de venteo (antorcha).',
    2,
    TRUE,
    'Si/No',
    'Dicotomica',
    'unica'
),
(
    9,
    NULL,
    'Registro trazable de los flujos másicos del gas piloto y de gas barrido',
    'Número de Fiscalizaciones a establecimientos que cuenten con sistemas de venteo en los que se realice quema controlada que den cuenta del registro trazable de los flujos másicos horarios del gas piloto y de gas de barrido.',
    2,
    TRUE,
    'Suma del número de fiscalizaciones a establecimiento que cuenten con sistema de venteo con quema controlada mediante antorcha',
    'Numero',
    'anual'
)
;
SELECT setval('proyecto_prevencion_medida_id_seq', (SELECT MAX(id) FROM proyecto_prevencion_medida));


-- Medida 1
INSERT INTO proyecto_prevencion_documentorequerido (medida_id, descripcion)
VALUES 
(1, 'Registro de las RCA aprobadas identificando el titular, la RCA, las emisiones y el monto a compensar');

-- Medida 2
INSERT INTO proyecto_prevencion_documentorequerido (medida_id, descripcion)
VALUES 
(2, 'Informe de Avance de Implementación de las medidas del Artículo 33 del Plan.'),
(2, 'En caso de solicitar más plazo, Oficio de envío de la Resolución que califica el Cronograma de implementación gradual para el plazo de cumplimiento');

-- Medida 3
INSERT INTO proyecto_prevencion_documentorequerido (medida_id, descripcion)
VALUES 
(3, 'Oficialización de la Instrucción de SEC para cumplir con el sistema indicado en el artículo 33 del Plan.');

-- Medida 4
INSERT INTO proyecto_prevencion_documentorequerido (medida_id, descripcion)
VALUES 
(4, 'Resolución que aprueba por la SEC, el sistema intermedio u otro que cumpla con el mismo objetivo');

-- Medida 5
INSERT INTO proyecto_prevencion_documentorequerido (medida_id, descripcion)
VALUES 
(5, 'Informe de Avance de Implementación de las medidas del Artículo 33 del Plan'),
(5, 'En caso de solicitar más plazo, Oficio de envio de la Resolución que califica el Cronograma de implementación gradual para el plazo de cumplimiento');

-- Medida 6
INSERT INTO proyecto_prevencion_documentorequerido (medida_id, descripcion)
VALUES 
(6, 'Programa de mantención y operación de los dispositivos y/o infraestructura, recepcionado hasta mayo de cada año a la SEC');

-- Medida 7
INSERT INTO proyecto_prevencion_documentorequerido (medida_id, descripcion)
VALUES 
(7, 'Registro interno del servicio con el número de fiscalizaciones ejecutadas a instalaciones de almacenamiento y distribución de combustibles líquidos'),
(7, 'Programa de mantención y operación de los dispositivos y/o infraestructura, recepcionado hasta mayo de cada año a la SEC');

-- Medida 8
INSERT INTO proyecto_prevencion_documentorequerido (medida_id, descripcion)
VALUES 
(8, 'Registro fotográfico del piloto de encendido manual y automático, enviado a la SEC.'),
(8, 'Registro del sistema de control de los sistemas de encendido, enviado a la SEC.');

-- Medida 9
INSERT INTO proyecto_prevencion_documentorequerido (medida_id, descripcion)
VALUES 
(9, 'Registro interno del servicio del número de fiscalizaciones donde se verificó el cumplimiento del registro trazable actualizado, en formato físico y digital');

SELECT setval('proyecto_prevencion_documentorequerido_id_seq', (SELECT MAX(id) FROM proyecto_prevencion_documentorequerido));