import api from "./api";
export const serviceService = {
    getServices,
    createService,
    contactServiceProvider
};

function getServices() {
	return api.get('api/v1.0/service/')
}

function createService(name, description) {
	return api.post('api/v1.0/service/', {name, description})	
}
function contactServiceProvider(service_id) {
	return api.patch(`api/v1.0/service/${service_id}/contact/`)	
}