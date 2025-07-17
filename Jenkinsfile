pipeline {
    agent any

    environment {
        DEPLOY_DIR = "/home/etl_toy/etl_app"
    }

    stages {
        stage('Git Pull') {
            steps {
                echo "최신 코드 가져오기..."
                script {
                    sh """
                        sudo -u jian

                        cd ${DEPLOY_DIR}
                        
                        # Git pull 실행 (에러 처리 포함)
                        sudo -u jian git pull origin master
                        echo "최신 커밋: \$(git log --oneline -1)"
                    """
                }
            }
        }

        stage('Deploy') {
            steps {
                echo "서비스 배포 시작..."
                script {
                    sh """
                        cd ${DEPLOY_DIR}
                        
                        # 스크립트 실행 권한 설정
                        sudo -u jian chmod +x run.sh 2>/dev/null || echo "run.sh 권한 설정 실패"
                        
                        # 배포 실행
                        sudo -u jian ./run.sh
                    """
                }
            }
        }

        stage('Health Check') {
            steps {
                echo "서비스 상태 확인..."
                script {
                    sh """
                        cd ${DEPLOY_DIR}
                        
                        # 서비스 시작 대기
                        echo "서비스 시작 대기 중..."
                        sleep 10
                        
                        # PostgreSQL 상태 확인
                        echo "=== PostgreSQL 상태 ==="
                        docker-compose -f docker-compose-db.yml ps
                        
                        # Airflow 상태 확인
                        echo "=== Airflow 상태 ==="
                        docker-compose ps

                        # Airflow Web UI 주소 안내
                        echo ""
                        echo "Airflow Web UI: http://localhost:9090"
                        echo "로그인: admin / admin"
                        echo "PostgreSQL: localhost:5434"
                        echo "DAG ID: air_quality_etl_pipeline"
                        echo ""
                        echo "유용한 명령어:"
                        echo "   로그 확인: docker-compose logs -f"
                        echo "   DB 로그 확인: docker-compose -f docker-compose-db.yml logs -f"
                        echo "   전체 중지: docker-compose down && docker-compose -f docker-compose-db.yml down"
                    """
                }
            }
        }
    }

    post {
        success {
            echo "배포 성공!"
            echo "Airflow Web UI: http://localhost:9090"
            echo "로그인: admin / admin"
            echo "PostgreSQL: localhost:5434"
            echo "DAG ID: air_quality_etl_pipeline"
        }
        failure {
            echo "배포 실패!"
            script {
                sh """
                    cd ${DEPLOY_DIR}
                    echo "=== 에러 진단 ==="
                    echo "현재 사용자: \$(whoami)"
                    echo "현재 디렉토리: \$(pwd)"
                    echo "Git 상태: \$(git status --porcelain)"
                    echo "Docker 상태: \$(docker ps -a | grep airflow)"
                    
                    # Airflow 로그 확인
                    echo "=== Airflow 웹서버 로그 ==="
                    docker logs \$(docker ps -a --filter 'name=airflow-webserver' --format '{{.Names}}') --tail 10 2>/dev/null || echo "Airflow 웹서버 로그 없음"
                    
                    # 파일 시스템 확인
                    echo "=== 파일 확인 ==="
                    ls -la ${DEPLOY_DIR} | head -10
                """
            }
        }
        always {
            echo "배포 프로세스 완료: \$(date)"
        }
    }
}
