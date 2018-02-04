import axios from 'axios';
import _ from 'lodash';
import { URL, LOGIN } from './config/api';

export function InvalidCredentialsException(message) {
    this.message = message;
    this.name = 'InvalidCredentialsException';
}

export  function login(username, password) {

    return axios
        .post(URL + LOGIN, {
            username,
            password
        })

        .catch(function (error) {
            // raise different exception if due to invalid credentials
            if (_.get(error, 'response.status') === 400) {
                throw new InvalidCredentialsException(error);
            }
            return false;
        });
}
