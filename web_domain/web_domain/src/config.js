const config = {
    development: {
        apiBaseUrl: 'http://localhost:5000'
    },
    production: {
        apiBaseUrl: 'http://localhost:5000'
    }
};

const currentEnv = process.env.NODE_ENV || 'development';
export const apiBaseUrl = config[currentEnv].apiBaseUrl;