# swagger_client.ConsumersApi

All URIs are relative to *https://virtserver.swaggerhub.com/khaug/public-name/1.0.0*

Method | HTTP request | Description
------------- | ------------- | -------------
[**search_public_name**](ConsumersApi.md#search_public_name) | **GET** /public-name | searches DToL public names

# **search_public_name**
> list[PublicName] search_public_name(search_string=search_string, skip=skip, limit=limit)

searches DToL public names

By passing in the appropriate options, you can search for available public names in the system 

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.ConsumersApi()
search_string = 'search_string_example' # str | pass an optional search string for looking up a public name (optional)
skip = 56 # int | number of records to skip for pagination (optional)
limit = 56 # int | maximum number of records to return (optional)

try:
    # searches DToL public names
    api_response = api_instance.search_public_name(search_string=search_string, skip=skip, limit=limit)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ConsumersApi->search_public_name: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **search_string** | **str**| pass an optional search string for looking up a public name | [optional] 
 **skip** | **int**| number of records to skip for pagination | [optional] 
 **limit** | **int**| maximum number of records to return | [optional] 

### Return type

[**list[PublicName]**](PublicName.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

