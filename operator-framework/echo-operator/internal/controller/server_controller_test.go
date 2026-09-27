package controller

import (
	"testing"

	appv1 "github.com/guymenahem/how-to-devops-tools/api/v1"

	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
	"k8s.io/apimachinery/pkg/runtime"
	clientgoscheme "k8s.io/client-go/kubernetes/scheme"
)

func testReconciler(t *testing.T) *EchoServerReconciler {
	t.Helper()

	scheme := runtime.NewScheme()
	if err := clientgoscheme.AddToScheme(scheme); err != nil {
		t.Fatalf("adding client-go scheme: %v", err)
	}
	if err := appv1.AddToScheme(scheme); err != nil {
		t.Fatalf("adding echoserver scheme: %v", err)
	}

	return &EchoServerReconciler{Scheme: scheme}
}

func testEchoServer(message string, size int32) *appv1.EchoServer {
	return &appv1.EchoServer{
		ObjectMeta: metav1.ObjectMeta{Name: "my-echo", Namespace: "default"},
		Spec:       appv1.EchoServerSpec{Message: message, Size: size},
	}
}

// The container args are exec'd without a shell, so quoting the message would
// make http-echo serve the quotes as part of the body.
func TestEchoDeploymentArgsAreNotShellQuoted(t *testing.T) {
	r := testReconciler(t)
	dep := r.echoDeployment(testEchoServer("My First Operator in Go!", 3))

	containers := dep.Spec.Template.Spec.Containers
	if len(containers) != 1 {
		t.Fatalf("expected 1 container, got %d", len(containers))
	}

	want := []string{"-listen=:8080", "-text=My First Operator in Go!"}
	got := containers[0].Args
	if len(got) != len(want) {
		t.Fatalf("args = %q, want %q", got, want)
	}
	for i := range want {
		if got[i] != want[i] {
			t.Errorf("args[%d] = %q, want %q", i, got[i], want[i])
		}
	}
}

func TestEchoDeploymentUsesSpecSize(t *testing.T) {
	r := testReconciler(t)
	dep := r.echoDeployment(testEchoServer("hello", 3))

	if dep.Spec.Replicas == nil {
		t.Fatal("replicas is nil")
	}
	if *dep.Spec.Replicas != 3 {
		t.Errorf("replicas = %d, want 3", *dep.Spec.Replicas)
	}
}

// The service selector has to match the labels the deployment stamps onto its
// pods, otherwise the service has no endpoints.
func TestEchoServiceSelectorMatchesDeploymentPodLabels(t *testing.T) {
	r := testReconciler(t)
	v := testEchoServer("hello", 1)

	podLabels := r.echoDeployment(v).Spec.Template.ObjectMeta.Labels
	selector := r.echoService(v).Spec.Selector

	for k, want := range selector {
		if got, ok := podLabels[k]; !ok || got != want {
			t.Errorf("pod labels %v do not satisfy service selector %v (key %q)", podLabels, selector, k)
		}
	}
	if selector["tier"] != "echo" {
		t.Errorf("selector tier = %q, want %q", selector["tier"], "echo")
	}
}

func TestEchoResourcesAreOwnedByTheCR(t *testing.T) {
	r := testReconciler(t)
	v := testEchoServer("hello", 1)

	for name, refs := range map[string][]metav1.OwnerReference{
		"deployment": r.echoDeployment(v).OwnerReferences,
		"service":    r.echoService(v).OwnerReferences,
	} {
		if len(refs) != 1 {
			t.Errorf("%s: expected 1 owner reference, got %d", name, len(refs))
			continue
		}
		if refs[0].Kind != "EchoServer" || refs[0].Name != v.Name {
			t.Errorf("%s: owner reference = %+v, want EchoServer/%s", name, refs[0], v.Name)
		}
	}
}
