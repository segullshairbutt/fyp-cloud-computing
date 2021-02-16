import { useEffect, useState } from 'react';
import produce from 'immer';

import axios from '../custom-axios';
import ProjectListComponent from '../../components/ProjectList';

const converErrorIntoArray = (err) => {
  if (err.response) {
    if (err.response.data) {
      if (err.response.data.error) {
        return [ err.response.data.error ];
      } else {
        const errorData = err.response.data;
        const keys = Object.keys(errorData);

        const allErrors = keys.map((key) => [ ...errorData[key].map((error) => key + ': ' + error) ]);
        return allErrors.flat(1);
      }
    }
  } else {
    return [ err.message ];
  }
};

const ProjectList = (props) => {
  const [ saved, setSaved ] = useState(false);
  const [ errors, setErrors ] = useState(null);
  const [ projects, setProjects ] = useState([]);

  useEffect(() => {
    axios
      .get('/api/projects/')
      .then((res) => {
        setProjects(res.data);
      })
      .catch((err) => setErrors(converErrorIntoArray(err)));
  }, []);

  const cancelButtonHandler = () => {
    setSaved(false);
    setErrors(null);
  };

  const projectSubmitHandler = (obj) => {
    axios
      .post('/api/projects/create/', obj)
      .then((res) => {
        setProjects(
          produce(projects, (draft) => {
            draft.push(res.data);
          })
        );
        setSaved(true);
      })
      .catch((err) => setErrors(converErrorIntoArray(err)));
  };

  const projectDeleteHandler = (id) => {
    axios
      .delete(`/api/projects/${id}/`)
      .then(() => {
        setProjects(
          produce(projects, (draft) => {
            const index = draft.findIndex((project) => project.id === id);            
            if (index !== -1) draft.splice(index, 1);
          })
        );
      })
      .catch((err) => setErrors(converErrorIntoArray(err)));
  };
  return (
    <ProjectListComponent
      projects={projects}
      submitErrors={errors}
      formSaved={saved}
      cancelClicked={cancelButtonHandler}
      formSubmitted={projectSubmitHandler}
      projectDeleted={projectDeleteHandler}
    />
  );
};

export default ProjectList;

const projects = [
  {
    id: 8,
    name: 'oa4_pet_store',
    username: 'admin',
    config: {
      tag: '01',
      code: {
        openapi: '3.0.0',
        info: {
          description:
            'This is a sample server Petstore server.  You can find out more about     Swagger at [http://swagger.io](http://swagger.io) or on [irc.freenode.net, #swagger](http://swagger.io/irc/).      For this sample, you can use the api key `special-key` to test the authorization     filters.',
          version: '1.0.0',
          title: 'Swagger Petstore',
          termsOfService: 'http://swagger.io/terms/',
          contact: {
            email: 'apiteam@swagger.io'
          },
          license: {
            name: 'Apache 2.0',
            url: 'http://www.apache.org/licenses/LICENSE-2.0.html'
          },
          'x-clusters': {
            cl1: {
              name: 'cl1',
              metrics: {
                load: ''
              },
              'worker-nodes': {
                wn1: {
                  metrics: {
                    load: ''
                  },
                  name: 'wn1',
                  pods: {
                    pod1: {
                      name: 'pod1',
                      metrics: {
                        load: ''
                      },
                      containers: {
                        c1: {
                          id: 'c1',
                          metrics: {
                            load: ''
                          }
                        },
                        c2: {
                          id: 'c2',
                          metrics: {
                            load: ''
                          }
                        },
                        c3: {
                          id: 'c3',
                          metrics: {
                            load: ''
                          }
                        },
                        c4: {
                          id: 'c4',
                          metrics: {
                            load: ''
                          }
                        }
                      }
                    }
                  }
                }
              }
            }
          }
        },
        servers: [
          {
            url: 'https://petstore.swagger.io',
            description: 'Optional server description, e.g. Main (production) server'
          }
        ],
        tags: [
          {
            name: 'pet',
            description: 'Everything about your Pets',
            externalDocs: {
              description: 'Find out more',
              url: 'http://swagger.io'
            }
          },
          {
            name: 'store',
            description: 'Access to Petstore orders'
          },
          {
            name: 'user',
            description: 'Operations about user',
            externalDocs: {
              description: 'Find out more about our store',
              url: 'http://swagger.io'
            }
          }
        ],
        paths: {
          '/pets': {
            post: {
              tags: [ 'pet' ],
              summary: 'Add a new pet to the store',
              description: '',
              requestBody: {
                description: 'description about addition to pet',
                required: true,
                content: {
                  'application/json': {
                    schema: {
                      $ref: '#/components/schemas/Pet'
                    }
                  }
                }
              },
              responses: {
                '405': {
                  description: 'Invalid input'
                }
              },
              security: [
                {
                  petstore_auth: [ 'write:pets', 'read:pets' ]
                }
              ],
              'x-metrics': {
                load: ''
              },
              'x-location': {
                $ref: '#/info/x-clusters/cl1/worker-nodes/wn1/pods/pod1/containers/c1'
              }
            },
            put: {
              tags: [ 'pet' ],
              summary: 'Update a pet to the store',
              description: '',
              requestBody: {
                description: 'description about updating the pet',
                required: true,
                content: {
                  'application/json': {
                    schema: {
                      $ref: '#/components/schemas/Pet'
                    }
                  }
                }
              },
              responses: {
                '405': {
                  description: 'Invalid input'
                }
              },
              security: [
                {
                  petstore_auth: [ 'write:pets', 'read:pets' ]
                }
              ],
              'x-metrics': {
                load: ''
              },
              'x-location': {
                $ref: '#/info/x-clusters/cl1/worker-nodes/wn1/pods/pod1/containers/c1'
              }
            },
            get: {
              tags: [ 'pet' ],
              summary: 'Get a pet from the store',
              description: '',
              responses: {
                '405': {
                  description: 'Invalid input'
                }
              },
              security: [
                {
                  petstore_auth: [ 'write:pets', 'read:pets' ]
                }
              ],
              'x-metrics': {
                load: ''
              },
              'x-location': {
                $ref: '#/info/x-clusters/cl1/worker-nodes/wn1/pods/pod1/containers/c2'
              }
            },
            delete: {
              tags: [ 'pet' ],
              summary: 'Delete a pet from the store',
              description: '',
              responses: {
                '405': {
                  description: 'Invalid input'
                }
              },
              security: [
                {
                  petstore_auth: [ 'write:pets', 'read:pets' ]
                }
              ],
              'x-metrics': {
                load: ''
              },
              'x-location': {
                $ref: '#/info/x-clusters/cl1/worker-nodes/wn1/pods/pod1/containers/c2'
              }
            }
          },
          '/store': {
            post: {
              tags: [ 'store' ],
              summary: 'Add a new store',
              description: '',
              requestBody: {
                description: 'description about addition to store',
                required: true,
                content: {
                  'application/json': {
                    schema: {
                      $ref: '#/components/schemas/Store'
                    }
                  }
                }
              },
              responses: {
                '405': {
                  description: 'Invalid input'
                }
              },
              security: [
                {
                  petstore_auth: [ 'write:pets', 'read:pets' ]
                }
              ],
              'x-metrics': {
                load: ''
              },
              'x-location': {
                $ref: '#/info/x-clusters/cl1/worker-nodes/wn1/pods/pod1/containers/c3'
              }
            },
            put: {
              tags: [ 'store' ],
              summary: 'Update the store',
              description: '',
              requestBody: {
                description: 'description about updating the store',
                required: true,
                content: {
                  'application/json': {
                    schema: {
                      $ref: '#/components/schemas/Store'
                    }
                  }
                }
              },
              responses: {
                '405': {
                  description: 'Invalid input'
                }
              },
              security: [
                {
                  petstore_auth: [ 'write:pets', 'read:pets' ]
                }
              ],
              'x-metrics': {
                load: ''
              },
              'x-location': {
                $ref: '#/info/x-clusters/cl1/worker-nodes/wn1/pods/pod1/containers/c3'
              }
            },
            get: {
              tags: [ 'store' ],
              summary: 'Get the store',
              description: '',
              responses: {
                '405': {
                  description: 'Invalid input'
                }
              },
              security: [
                {
                  petstore_auth: [ 'write:pets', 'read:pets' ]
                }
              ],
              'x-metrics': {
                load: ''
              },
              'x-location': {
                $ref: '#/info/x-clusters/cl1/worker-nodes/wn1/pods/pod1/containers/c2'
              }
            },
            delete: {
              tags: [ 'store' ],
              summary: 'Delete a store',
              description: '',
              responses: {
                '405': {
                  description: 'Invalid input'
                }
              },
              security: [
                {
                  petstore_auth: [ 'write:pets', 'read:pets' ]
                }
              ],
              'x-metrics': {
                load: ''
              },
              'x-location': {
                $ref: '#/info/x-clusters/cl1/worker-nodes/wn1/pods/pod1/containers/c2'
              }
            }
          },
          '/user': {
            post: {
              tags: [ 'user' ],
              summary: 'Add a new User',
              description: '',
              requestBody: {
                description: 'description about addition of User',
                required: true,
                content: {
                  'application/json': {
                    schema: {
                      $ref: '#/components/schemas/User'
                    }
                  }
                }
              },
              responses: {
                '405': {
                  description: 'Invalid input'
                }
              },
              security: [
                {
                  petstore_auth: [ 'write:pets', 'read:pets' ]
                }
              ],
              'x-metrics': {
                load: ''
              },
              'x-location': {
                $ref: '#/info/x-clusters/cl1/worker-nodes/wn1/pods/pod1/containers/c4'
              }
            },
            put: {
              tags: [ 'user' ],
              summary: 'Update the store',
              description: '',
              requestBody: {
                description: 'description about updating the User',
                required: true,
                content: {
                  'application/json': {
                    schema: {
                      $ref: '#/components/schemas/User'
                    }
                  }
                }
              },
              responses: {
                '405': {
                  description: 'Invalid input'
                }
              },
              security: [
                {
                  petstore_auth: [ 'write:pets', 'read:pets' ]
                }
              ],
              'x-metrics': {
                load: ''
              },
              'x-location': {
                $ref: '#/info/x-clusters/cl1/worker-nodes/wn1/pods/pod1/containers/c4'
              }
            },
            get: {
              tags: [ 'user' ],
              summary: 'Get the user',
              description: '',
              responses: {
                '405': {
                  description: 'Invalid input'
                }
              },
              security: [
                {
                  petstore_auth: [ 'write:pets', 'read:pets' ]
                }
              ],
              'x-metrics': {
                load: ''
              },
              'x-location': {
                $ref: '#/info/x-clusters/cl1/worker-nodes/wn1/pods/pod1/containers/c2'
              }
            },
            delete: {
              tags: [ 'user' ],
              summary: 'Delete a user',
              description: '',
              responses: {
                '405': {
                  description: 'Invalid input'
                }
              },
              security: [
                {
                  petstore_auth: [ 'write:pets', 'read:pets' ]
                }
              ],
              'x-metrics': {
                load: ''
              },
              'x-location': {
                $ref: '#/info/x-clusters/cl1/worker-nodes/wn1/pods/pod1/containers/c2'
              }
            }
          }
        },
        components: {
          securitySchemes: {
            petstore_auth: {
              type: 'oauth2',
              flows: {
                authorizationCode: {
                  authorizationUrl: '/oauth/dialog',
                  tokenUrl: '/oauth/token',
                  scopes: {
                    'write:pets': 'modify pets in your account',
                    'read:pets': 'read your pets'
                  }
                }
              }
            },
            api_key: {
              type: 'apiKey',
              name: 'api_key',
              in: 'header'
            }
          },
          schemas: {
            Pet: {
              type: 'object',
              required: [ 'name', 'photoUrls' ],
              properties: {
                id: {
                  type: 'integer',
                  format: 'int64'
                },
                category: {
                  $ref: '#/components/schemas/Category'
                },
                name: {
                  type: 'string',
                  example: 'doggie'
                },
                photoUrls: {
                  type: 'array',
                  xml: {
                    name: 'photoUrl',
                    wrapped: true
                  },
                  items: {
                    type: 'string'
                  }
                },
                tags: {
                  type: 'array',
                  xml: {
                    name: 'tag',
                    wrapped: true
                  },
                  items: {
                    $ref: '#/components/schemas/Tag'
                  }
                },
                status: {
                  type: 'string',
                  description: 'pet status in the store',
                  enum: [ 'available', 'pending', 'sold' ]
                }
              },
              xml: {
                name: 'Pet'
              },
              'x-storage-level': 'pod'
            },
            Store: {
              type: 'object',
              required: [ 'name' ],
              properties: {
                id: {
                  type: 'integer',
                  format: 'int64'
                },
                name: {
                  type: 'string',
                  example: 'franchise'
                },
                status: {
                  type: 'string',
                  description: 'store status',
                  enum: [ 'open', 'closed' ]
                }
              },
              xml: {
                name: 'Store'
              },
              'x-storage-level': 'pod'
            },
            Tag: {
              type: 'object',
              properties: {
                id: {
                  type: 'integer',
                  format: 'int64'
                },
                name: {
                  type: 'string'
                }
              },
              xml: {
                name: 'Tag'
              },
              'x-storage-level': 'pod'
            },
            Category: {
              type: 'object',
              properties: {
                id: {
                  type: 'integer',
                  format: 'int64'
                },
                name: {
                  type: 'string'
                }
              },
              xml: {
                name: 'Category'
              },
              'x-storage-level': 'pod'
            },
            User: {
              type: 'object',
              properties: {
                id: {
                  type: 'integer',
                  format: 'int64'
                },
                username: {
                  type: 'string'
                },
                password: {
                  type: 'string'
                }
              },
              xml: {
                name: 'User'
              },
              'x-storage-level': 'pod'
            }
          }
        },
        externalDocs: {
          description: 'Find out more about Swagger',
          url: 'http://swagger.io'
        }
      }
    }
  }
];
