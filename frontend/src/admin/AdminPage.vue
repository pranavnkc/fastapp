<template>
    <div>
        <form @submit.prevent="onSubmit">
            <div class="form-group">
                <label for="Title">Name</label>
                <input type="text" v-model.trim="$v.name.$model" name="name" class="form-control" :class="{ 'is-invalid': submitted && $v.name.$error }" />
                <div v-if="submitted && !$v.name.required" class="invalid-feedback">Name is required</div>
            </div>
            <div class="form-group">
                <label htmlFor="description">Description</label>
                <input type="text" v-model.trim="$v.description.$model" name="description" class="form-control" :class="{ 'is-invalid': submitted && $v.description.$error }" />
                <div v-if="submitted && !$v.description.required" class="invalid-feedback">Description is required</div>
            </div>
            <div class="form-group">
                <button class="btn btn-primary" :disabled="loading">
                    <span class="spinner-border spinner-border-sm" v-show="loading"></span>
                    <span>Create</span>
                </button>
            </div>
            <div v-if="error" class="alert alert-danger">{{error}}</div>
        </form>
    </div>
</template>

<script>
import { authenticationService, serviceService } from '@/_services';
import { required } from 'vuelidate/lib/validators';
import { router } from '@/_helpers';


export default {
    data () {
        return {
            user: authenticationService.currentUserValue,
            users: [],
            name: '',
            description: '',
            submitted: false,
            loading: false,
            returnUrl: '',
            error: ''
        };
    },
    validations: {
      name: { required },
      description: { required }
    },
    methods: {
        onSubmit () {
            this.submitted = true;
            // stop here if form is invalid
            this.$v.$touch();
            if (this.$v.$invalid) {
                return;
            }

            this.loading = true;
            serviceService.createService(this.name, this.description)
                .then(
                    res => router.push('/'),
                    error => {
                        this.error = error['data'];
                        this.loading = false;
                    }
                );
        }
    }
};
</script>