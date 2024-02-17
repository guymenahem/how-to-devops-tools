package controller

import (
	"context"
	"time"

	appv1 "github.com/guymenahem/how-to-devops-tools/api/v1"

	appsv1 "k8s.io/api/apps/v1"
	corev1 "k8s.io/api/core/v1"
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
	"k8s.io/apimachinery/pkg/types"
	"k8s.io/apimachinery/pkg/util/intstr"
	"sigs.k8s.io/controller-runtime/pkg/controller/controllerutil"
	"sigs.k8s.io/controller-runtime/pkg/reconcile"
)

const echoPort = 8080
const echoImage = "hashicorp/http-echo"

func echoDeploymentName(v *appv1.EchoServer) string {
	return v.Name + "-echo"
}

func echoServiceName(v *appv1.EchoServer) string {
	return v.Name + "-echo-service"
}

func (r *EchoServerReconciler) echoDeployment(v *appv1.EchoServer) *appsv1.Deployment {
	labels := labels(v, "echo")
	size := v.Spec.Size
	message := v.Spec.Message

	dep := &appsv1.Deployment{
		ObjectMeta: metav1.ObjectMeta{
			Name:      echoDeploymentName(v),
			Namespace: v.Namespace,
		},
		Spec: appsv1.DeploymentSpec{
			Replicas: &size,
			Selector: &metav1.LabelSelector{
				MatchLabels: labels,
			},
			Template: corev1.PodTemplateSpec{
				ObjectMeta: metav1.ObjectMeta{
					Labels: labels,
				},
				Spec: corev1.PodSpec{
					Containers: []corev1.Container{{
						Image:           echoImage,
						ImagePullPolicy: corev1.PullAlways,
						Name:            "echo-server",
						Ports: []corev1.ContainerPort{{
							ContainerPort: echoPort,
							Name:          "echo-server",
						}},
						Args: []string{
							"-listen=:8080",
							"-text='" + message + "'",
						},
					}},
				},
			},
		},
	}

	controllerutil.SetControllerReference(v, dep, r.Scheme)
	return dep
}

func (r *EchoServerReconciler) echoService(v *appv1.EchoServer) *corev1.Service {
	labels := labels(v, "echo")

	s := &corev1.Service{
		ObjectMeta: metav1.ObjectMeta{
			Name:      echoServiceName(v),
			Namespace: v.Namespace,
		},
		Spec: corev1.ServiceSpec{
			Selector: labels,
			Ports: []corev1.ServicePort{{
				Protocol:   corev1.ProtocolTCP,
				Port:       echoPort,
				TargetPort: intstr.FromInt(echoPort),
			}},
			Type: corev1.ServiceTypeClusterIP,
		},
	}

	controllerutil.SetControllerReference(v, s, r.Scheme)
	return s
}

func (r *EchoServerReconciler) updateEchoStatus(v *appv1.EchoServer) error {
	v.Status.EchoStatus = "Ready"
	err := r.Client.Status().Update(context.TODO(), v)
	return err
}

func (r *EchoServerReconciler) handleEchoChanges(v *appv1.EchoServer) (*reconcile.Result, error) {
	found := &appsv1.Deployment{}
	err := r.Client.Get(context.TODO(), types.NamespacedName{
		Name:      echoDeploymentName(v),
		Namespace: v.Namespace,
	}, found)
	if err != nil {
		// The deployment may not have been created yet, so requeue
		return &reconcile.Result{RequeueAfter: 5 * time.Second}, err
	}

	size := v.Spec.Size

	if size != *found.Spec.Replicas {
		found.Spec.Replicas = &size
		err = r.Client.Update(context.TODO(), found)
		if err != nil {
			log.Error(err, "Failed to update Deployment.", "Deployment.Namespace", found.Namespace, "Deployment.Name", found.Name)
			return &reconcile.Result{}, err
		}
		// Spec updated - return and requeue
		return &reconcile.Result{Requeue: true}, nil
	}

	return nil, nil
}
