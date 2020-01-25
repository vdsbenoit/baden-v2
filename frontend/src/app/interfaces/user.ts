
export interface User {
   uid: string;
   username: string;
   email: string;
   emailVerified: boolean;
   permissions: string[];
   inscription: Date;
}
