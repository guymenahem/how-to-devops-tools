package controller

import (
	"context"
	"fmt"
	"time"

	appv1 "github.com/guymenahem/how-to-devops-tools/api/v1"

	appsv1 "k8s.io/api/apps/v1"
	corev1 "k8s.io/api/core/v1"
	"k8s.io/apimachinery/pkg/api/equality"
	"k8s.io/apimachinery/pkg/api/errors"
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

// echoArgs builds the http-echo command line. Container args are exec'd
// without a shell, so the message must not be wrapped in quotes.
func echoArgs(message string) []string {
	return []string{
		fmt.Sprintf("-listen=:%d", echoPort),
		"-text=" + message,
	}
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
						Args: echoArgs(message),
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

func (r *EchoServerReconciler) updateEchoStatus(ctx context.Context, v *appv1.EchoServer) error {
	status := "Pending"

	found := &appsv1.Deployment{}
	err := r.Client.Get(ctx, types.NamespacedName{
		Name:      echoDeploymentName(v),
		Namespace: v.Namespace,
	}, found)
	if err == nil && found.Status.ReadyReplicas == v.Spec.Size {
		status = "Ready"
	}

	if v.Status.EchoStatus == status {
		return nil
	}

	v.Status.EchoStatus = status
	return r.Client.Status().Update(ctx, v)
}

func (r *EchoServerReconciler) handleEchoChanges(ctx context.Context, v *appv1.EchoServer) (*reconcile.Result, error) {
	found := &appsv1.Deployment{}
	err := r.Client.Get(ctx, types.NamespacedName{
		Name:      echoDeploymentName(v),
		Namespace: v.Namespace,
	}, found)
	if err != nil {
		if errors.IsNotFound(err) {
			// The deployment may not have hit the cache yet, so just requeue.
			return &reconcile.Result{RequeueAfter: 5 * time.Second}, nil
		}
		return &reconcile.Result{}, err
	}

	size := v.Spec.Size
	desiredArgs := echoArgs(v.Spec.Message)

	changed := false
	if found.Spec.Replicas == nil || size != *found.Spec.Replicas {
		found.Spec.Replicas = &size
		changed = true
	}
	// Without this a change to spec.message is never rolled out.
	containers := found.Spec.Template.Spec.Containers
	if len(containers) > 0 && !equality.Semantic.DeepEqual(containers[0].Args, desiredArgs) {
		containers[0].Args = desiredArgs
		changed = true
	}

	if changed {
		if err := r.Client.Update(ctx, found); err != nil {
			log.Error(err, "Failed to update Deployment.", "Deployment.Namespace", found.Namespace, "Deployment.Name", found.Name)
			return &reconcile.Result{}, err
		}
		// Spec updated - return and requeue
		return &reconcile.Result{Requeue: true}, nil
	}

	return nil, nil
}
