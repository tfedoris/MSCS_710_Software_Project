import { ModelInit, MutableModel, PersistentModelConstructor } from "@aws-amplify/datastore";





export declare class UserRegistrationKey {
  readonly id: string;
  readonly userName: string;
  readonly key: string;
  readonly registrationId?: string;
  constructor(init: ModelInit<UserRegistrationKey>);
  static copyOf(source: UserRegistrationKey, mutator: (draft: MutableModel<UserRegistrationKey>) => MutableModel<UserRegistrationKey> | void): UserRegistrationKey;
}