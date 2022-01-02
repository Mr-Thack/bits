#include <stdio.h>

int trash()
{
	int a = 2;
	int b = a * a;
	a = b / (a*a);
	return a*b;
}

int main()
{
	int a = trash();
	printf("Hello\n");
	return 0;
}
