# swagger_client.CuratorsApi

All URIs are relative to *https://virtserver.swaggerhub.com/khaug/public-name/1.0.0*

Method | HTTP request | Description
------------- | ------------- | -------------
[**add_public_name**](CuratorsApi.md#add_public_name) | **POST** /public-name | adds a public name

# **add_public_name**
> add_public_name(body=body)

adds a public name

Adds a new public name to the system

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.CuratorsApi()
body = swagger_client.PublicName() # PublicName | Public name to add (optional)

try:
    # adds a public name
    api_instance.add_public_name(body=body)
except ApiException as e:
    print("Exception when calling CuratorsApi->add_public_name: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**PublicName**](PublicName.md)| Public name to add | [optional] 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

