/*
Copyright 2024.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
*/

package controller

import (
	"context"
	"k8s.io/apimachinery/pkg/api/errors"
	"k8s.io/apimachinery/pkg/runtime"
	ctrl "sigs.k8s.io/controller-runtime"
	"sigs.k8s.io/controller-runtime/pkg/client"
	ctrllog "sigs.k8s.io/controller-runtime/pkg/log"

	appv1 "github.com/guymenahem/how-to-devops-tools/api/v1"
)

var log = ctrllog.Log.WithName("controller_echoserver")

// EchoServerReconciler reconciles a EchoServer object
type EchoServerReconciler struct {
	client.Client
	Scheme *runtime.Scheme
}

//+kubebuilder:rbac:groups=demo.thegoodguy.io,resources=echoservers,verbs=get;list;watch;create;update;patch;delete
//+kubebuilder:rbac:groups=demo.thegoodguy.io,resources=echoservers/status,verbs=get;update;patch
//+kubebuilder:rbac:groups=demo.thegoodguy.io,resources=echoservers/finalizers,verbs=update
//+kubebuilder:rbac:groups=cache.example.com,resources=memcacheds,verbs=get;list;watch;create;update;patch;delete
//+kubebuilder:rbac:groups=cache.example.com,resources=memcacheds/status,verbs=get;update;patch
//+kubebuilder:rbac:groups=cache.example.com,resources=memcacheds/finalizers,verbs=update
//+kubebuilder:rbac:groups=core,resources=events,verbs=create;patch
//+kubebuilder:rbac:groups=apps,resources=deployments,verbs=get;list;watch;create;update;patch;delete
//+kubebuilder:rbac:groups=core,resources=services,verbs=get;list;watch;create;update;patch;delete
//+kubebuilder:rbac:groups=core,resources=pods,verbs=get;list;watch

// Reconcile is part of the main kubernetes reconciliation loop which aims to
// move the current state of the cluster closer to the desired state.
// TODO(user): Modify the Reconcile function to compare the state specified by
// the EchoServer object against the actual cluster state, and then
// perform operations to make the cluster state reflect the state specified by
// the user.
//
// For more details, check Reconcile and its Result here:
// - https://pkg.go.dev/sigs.k8s.io/controller-runtime@v0.15.0/pkg/reconcile
func (r *EchoServerReconciler) Reconcile(ctx context.Context, req ctrl.Request) (ctrl.Result, error) {
	log := ctrllog.FromContext(ctx)

	log.Info("Reconciling EchoServer", "Request.Namespace", req.Namespace, "Request.Name", req.Name)

	// Fetch the EchoServer instance
	v := &appv1.EchoServer{}
	err := r.Client.Get(context.TODO(), req.NamespacedName, v)
	if err != nil {
		if errors.IsNotFound(err) {
			// Request object not found, could have been deleted after ctrl req.
			// Owned objects are automatically garbage collected. For additional cleanup logic use finalizers.
			// Return and don't requeue
			return ctrl.Result{}, nil
		}
		// Error reading the object - requeue the req.
		return ctrl.Result{}, err
	}

	var result *ctrl.Result

	result, err = r.ensureDeployment(req, v, r.echoDeployment(v))
	if result != nil {
		return *result, err
	}

	result, err = r.ensureService(req, v, r.echoService(v))
	if result != nil {
		return *result, err
	}

	err = r.updateEchoStatus(v)
	if err != nil {
		// Requeue the req if the status could not be updated
		return ctrl.Result{}, err
	}

	result, err = r.handleEchoChanges(v)
	if result != nil {
		return *result, err
	}

	return ctrl.Result{}, nil
}

// SetupWithManager sets up the controller with the Manager.
func (r *EchoServerReconciler) SetupWithManager(mgr ctrl.Manager) error {
	return ctrl.NewControllerManagedBy(mgr).
		For(&appv1.EchoServer{}).
		Complete(r)
}
