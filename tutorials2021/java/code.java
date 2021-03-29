public static int foo(int[] arr)
{
	int m = arr[0];
	for (int i=1; i<arr.length; i++)
	{
		if (arr[i] > m)
			m = arr[i];
	}
	return m;
}
if (arr[i] < m)

public static boolean bar(int n)
{
	if (n < 2 || (n % 2 == 0 && n != 2))
		return false;

	int i = 3;
	while (i < n)
	{
		if (n % i == 0)
			return false;
		i = i + 2;
	}
	return true;
}

public static int baz(int n)
{
	int x = 1;
	for (i=1; i<=n; i++)
	{
		x = x * i;
	}
	return x;
}

public static int[] Q1(int[] arr)
{
	int n = arr.length;
	int arr2[] = new int[n];

	for (int i=0; i<n; i++)
		arr2[i] = arr[n-i-1];

	return arr2;
}

public static boolean Q2(int[] arr1, int[] arr2)
{
	if (arr1.length != arr2.length)
		return false;

	boolean condition = true;
	int i = 0;
	while (condition==true && i<arr1.length)
	{
		if (arr1[i] != arr2[i])
			condition = false;
		i++;
	}

	return condition;
}

public static int[] Fib(int n)
{
	int fibArray[] = new int[n+1];
	fibArray[0] = 1;
	fibArray[1] = 1;
	for (int i=2; i<=n; i++)
		fibArray[i] = fibArray[i-2] + fibArray[i-1];

	return fibArray;
}

public static int Fib2(int n)
{
	if (n==0) return 1;
	if (n==1) return 1;
	return Fib2(n-2) + Fib2(n-1);
}
