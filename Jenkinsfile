pipeline {
    agent any
    
    environment {
        // Define environment variables if needed
    }
    
    stages {
        stage('Checkout SCM') {
            steps {
                // Adjust this to match the location of your repository
                git url: 'url-to-your-git-repo', branch: 'main'
            }
        }

        stage('OWASP DependencyCheck') {
            steps {
                // Make sure the OWASP Dependency Check plugin is installed and configured
                dependencyCheck additionalArguments: '--format HTML --format XML', odcInstallation: 'Default'
            }
        }

        stage('Integration and UI Tests') {
            parallel {
                stage('Deploy and Integration Test') {
                    steps {
                        // Replace with the actual command/script to deploy your application
                        sh './deploy-to-test-environment.sh'
                        // Replace with actual integration test command
                        sh './run-integration-tests.sh'
                    }
                }
                stage('Headless Browser UI Test') {
                    agent {
                        docker {
                            image 'maven:3-alpine'
                            args '-v /root/.m2:/root/.m2'
                        }
                    }
                    steps {
                        // Assuming your UI tests are part of your Maven build
                        sh 'mvn -B -DskipTests clean package'
                        sh 'mvn test'
                    }
                    post {
                        always {
                            // Collects the JUnit test results
                            junit 'target/surefire-reports/*.xml'
                        }
                    }
                }
            }
        }
    }
    
    post {
        success {
            // This will publish the results of the OWASP Dependency Check
            dependencyCheckPublisher pattern: '**/dependency-check-report.xml'
            // You can also add notifications, etc. here if required
        }
    }
}
