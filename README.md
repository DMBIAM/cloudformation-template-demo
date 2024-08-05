# Implementación CloudFormation

El siguiente proyecto, tiene como objetivo implementar un template para AWS cloudformation que permita la integración de diferentes recursos trabajando de forma conjunta

A continuación se detalla en un diagrama la arquitectura utilizada para el ejercicio

![Arquitectura](https://github.com/DMBIAM/cloudformation-template-demo/blob/main/pic/arq.jpg)

# Características de arquitectura.

1.	Template en cloudformation que contiene la infraestructura ilustrada en la imagen referente a la arquitectura. 
2.	Los recursos correspondientes a networking como lo son la subnet solo se referencian más no se construyen.
3.	Los recursos indicados en el diagrama como lo son el rol, apigateway, lambdas, s3 cloudfront y dynamos se implementan y se crean mediante el template. 
4.	Definición de tag llamado “lm_troux_uid=123” a cada recurso creado.
5.	El cloudfront tendrá en su origin un archivo “index.html” de tal manera que al acceder al dominio del cloudfront, permitirá visualizar el contenido del html a modo de corroborar el funcionamiento.
6.	Para la base de datos dynamoDB el partition Key será Id de tipo numérico y el  sortKey Nombre tipo string
7.	Se creará una tabla en dynamoDB llamada productos, en la cual se agregan dos registros con la siguiente información.
{"Id": { "N": "1"}, "Nombre": {"S": "Tomate"}, "Cantidad": {"N": "10"}}
{"Id": { "N": "2"}, "Nombre": {"S": "Cebolla"}, " Cantidad ": {"N": "5"}}
8.	Se implementará un ApiGateway de tipo Rest, el cual solo contará con dos métodos, un método GET que permita listar los registros de la tabla productos en un json y uno tipo POST que permita listar los objetos del S3, este último tendrá un api key para validar cada petición que reciba. 
9.	Se construirá una lambda llamada listars3, la cual solo tendrá permisos de lectura de objetos del bucket s3demo.
10.	Se construirá una lambda llamada listardynamo, esta solo tendrá permisos de lectura desde dicha lambda. 
11.	El bucket s3 solo permitirá el acceso desde el cloudfront y desde las lambdas o el rol de las lambdas, no tendrá acceso público. 
12.	Para el runtime de las lambdas se utilizará Python. 

# Pasos para la implementación de la arquitectura

## Creación del template de CloudFormation:

### Versión y Descripción del Template:

- AWSTemplateFormatVersion: Se establece la versión del formato de CloudFormation.
- Description: Proporciona una breve descripción del template.


### Parámetros:

- VpcId: Parámetro para el ID de la VPC donde se implementarán los recursos.
- SubnetId: Parámetro para el ID de la Subnet donde se implementarán las Lambdas.
- TagKey: Key para los tag de cada recurso.
- TagValue: Valor de los tags para los recursos a implementar.

### Recursos:

#### S3Bucket:

- Creación de un bucket S3 llamado s3demo.
- Se añaden etiquetas (tags) al bucket.

#### S3BucketPolicy:

- Se define una política de bucket para s3demo.
- Se deniega el acceso no seguro (sin HTTPS).
- Se permite el acceso a objetos del bucket desde el rol iamRoleDemo y la identidad de acceso de origen de CloudFront.

#### CloudFrontOriginAccessIdentity:

- Creación de una identidad de acceso de origen para CloudFront para permitir el acceso al bucket S3 desde CloudFront.

#### CloudFrontDistribution:

- Configuración de una distribución de CloudFront para servir contenido desde el bucket S3.
- Se configura el comportamiento de caché predeterminado y el objeto raíz predeterminado (index.html).
- Se añaden etiquetas a la distribución de CloudFront.

#### DynamoDBTable:

- Creación de una tabla DynamoDB llamada productos.
- Definición de los atributos (Id y Nombre) y la clave principal de la tabla.
- Configuración del throughput provisionado para la tabla.
- Se añaden etiquetas a la tabla.

#### DynamoDBSeedData:

- Creación de una función Lambda llamada SeedDynamoDB para insertar datos iniciales en la tabla DynamoDB.
- Código inline para la función Lambda que inserta datos en la tabla productos.
- Configuración de la VPC y subnets donde se ejecutará la Lambda.
- Se añaden etiquetas a la función Lambda.

#### LambdaExecutionRole:

- Creación de un rol IAM llamado iamRoleDemo para las funciones Lambda.
- Política para asumir el rol por el servicio Lambda.
- Políticas para permitir a las Lambdas acceder a objetos en el bucket S3 y realizar operaciones en la tabla DynamoDB productos.
- Se añaden etiquetas al rol IAM.

#### ListarS3Lambda:

- Creación de una función Lambda llamada listarS3 para listar objetos en el bucket S3.
- Configuración del rol IAM (iamRoleDemo) para la Lambda.
- Especificación del bucket S3 y la clave del código Lambda.
- Configuración de la VPC y subnets donde se ejecutará la Lambda.
- Se añaden etiquetas a la función Lambda.

#### ListarDynamoLambda:

- Creación de una función Lambda llamada listarDynamo para listar items en la tabla DynamoDB.
- Configuración del rol IAM (iamRoleDemo) para la Lambda.
- Especificación del bucket S3 y la clave del código Lambda.
- Configuración de la VPC y subnets donde se ejecutará la Lambda.
- Se añaden etiquetas a la función Lambda.

#### ApiGateway:

- Creación de una API Gateway llamada APIGatewayDemo.
- Se añaden etiquetas a la API Gateway.

#### GetProductsMethod:

- Creación de un método GET en la API Gateway para invocar la función Lambda listarDynamo.
- Configuración de la integración AWS_PROXY para la invocación de la Lambda.
- Se añaden etiquetas al método.

#### ListS3ObjectsMethod:

- Creación de un método POST en la API Gateway para invocar la función Lambda listarS3.
- Requiere una API Key para la invocación.
- Configuración de la integración AWS_PROXY para la invocación de la Lambda.
- Se añaden etiquetas al método.

#### ApiKey:

- Creación de una API Key llamada DemoApiKey para la API Gateway.
- Asociación de la API Key con el stage prod de la API Gateway.
- Se añaden etiquetas a la API Key.

#### UploadIndexHtmlLambda: 

- Define una función Lambda para subir el archivo index.html al bucket S3.

#### UploadIndexHtmlCustomResource: 

- Utiliza un recurso personalizado para ejecutar la función Lambda UploadIndexHtmlLambda al crear el stack.

#### Salidas:

- CloudFrontURL: Proporciona la URL de la distribución de CloudFront.

El template cloudformation-template.yml, asegura que los recursos dispuestos en el diagrama de arquitectura cloud se configuren adecuadamente y que se cumplan los requisitos de seguridad y acceso especificados.



aws cloudformation create-stack --stack-name my-stack --template-body file://template.yaml --parameters ParameterKey=LambdaCodeBucket,ParameterValue=my-bucket-name ParameterKey=LambdaCodeKey,ParameterValue=my-code-path.zip


# Workflow GithubAction

- File: .github\workflows\deploy-lambda.yml
- Checkout Code: Clona el repositorio para que GitHub Actions pueda acceder a tu código.
- Set up AWS CLI: Configura AWS CLI con las credenciales necesarias para realizar despliegues.

## Package listarDynamo Lambda:

- Crea un directorio temporal (listarDynamo).
- Copia el archivo listarDynamo.py al directorio.
- Empaqueta el contenido del directorio en un archivo .zip.

## Package listarS3 Lambda:

- Crea un directorio temporal (listarS3).
- Copia el archivo listarS3.py al directorio.
- Empaqueta el contenido del directorio en un archivo .zip.

## Deploy listarDynamo Lambda:

- Usa el archivo .zip empaquetado para actualizar la función Lambda llamada listarDynamo.

## Deploy listarS3 Lambda:

- Usa el archivo .zip empaquetado para actualizar la función Lambda llamada listarS3.



