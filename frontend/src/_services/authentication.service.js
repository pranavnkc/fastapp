import { BehaviorSubject } from 'rxjs';
import api from "./api";

const currentUserSubject = new BehaviorSubject(JSON.parse(localStorage.getItem('currentUser')));

export const authenticationService = {
    login,
    logout,
    currentUser: currentUserSubject.asObservable(),
    get currentUserValue () { return currentUserSubject.value }
};

function login(username, password) {
    console.log(username, password, api)
    return api.post('api/v1.0/login/', { username, password })
        .then(user => {
            user = user.data
            // store user details and jwt token in local storage to keep user logged in between page refreshes
            user.role = user.user.groups[0];
            localStorage.setItem('currentUser', JSON.stringify(user));
            localStorage.setItem('access_token', user.token);
            currentUserSubject.next(user);
            return user;
        });
}

function logout() {
    // remove user from local storage to log user out
    localStorage.removeItem('currentUser');
    currentUserSubject.next(null);
}
