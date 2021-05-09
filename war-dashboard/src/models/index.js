// @ts-check
import { initSchema } from '@aws-amplify/datastore';
import { schema } from './schema';



const { UserRegistrationKey } = initSchema(schema);

export {
  UserRegistrationKey
};