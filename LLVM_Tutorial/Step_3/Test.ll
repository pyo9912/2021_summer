; ModuleID = 'Test.c'
source_filename = "Test.c"
target datalayout = "e-m:e-i64:64-f80:128-n8:16:32:64-S128"
target triple = "x86_64-unknown-linux-gnu"

@.str = private unnamed_addr constant [4 x i8] c"%f\0A\00", align 1

; Function Attrs: noinline nounwind optnone uwtable
define void @init(float*, float*, float*, i64) #0 {
  %5 = alloca float*, align 8
  %6 = alloca float*, align 8
  %7 = alloca float*, align 8
  %8 = alloca i64, align 8
  %9 = alloca i64, align 8
  store float* %0, float** %5, align 8
  store float* %1, float** %6, align 8
  store float* %2, float** %7, align 8
  store i64 %3, i64* %8, align 8
  store i64 0, i64* %9, align 8
  br label %10

; <label>:10:                                     ; preds = %38, %4
  %11 = load i64, i64* %9, align 8
  %12 = load i64, i64* %8, align 8
  %13 = icmp ult i64 %11, %12
  br i1 %13, label %14, label %41

; <label>:14:                                     ; preds = %10
  %15 = load i64, i64* %8, align 8
  %16 = load i64, i64* %9, align 8
  %17 = sub i64 %15, %16
  %18 = uitofp i64 %17 to float
  %19 = load float*, float** %5, align 8
  %20 = load i64, i64* %9, align 8
  %21 = getelementptr inbounds float, float* %19, i64 %20
  store float %18, float* %21, align 4
  %22 = load i64, i64* %8, align 8
  %23 = load i64, i64* %8, align 8
  %24 = add i64 %22, %23
  %25 = load i64, i64* %9, align 8
  %26 = add i64 %24, %25
  %27 = uitofp i64 %26 to float
  %28 = load float*, float** %6, align 8
  %29 = load i64, i64* %9, align 8
  %30 = getelementptr inbounds float, float* %28, i64 %29
  store float %27, float* %30, align 4
  %31 = load i64, i64* %9, align 8
  %32 = load i64, i64* %8, align 8
  %33 = add i64 %31, %32
  %34 = uitofp i64 %33 to float
  %35 = load float*, float** %7, align 8
  %36 = load i64, i64* %9, align 8
  %37 = getelementptr inbounds float, float* %35, i64 %36
  store float %34, float* %37, align 4
  br label %38

; <label>:38:                                     ; preds = %14
  %39 = load i64, i64* %9, align 8
  %40 = add i64 %39, 1
  store i64 %40, i64* %9, align 8
  br label %10

; <label>:41:                                     ; preds = %10
  ret void
}

; Function Attrs: noinline nounwind optnone uwtable
define void @VectorAdd(float*, float*, float*, i64) #0 {
  %5 = alloca float*, align 8
  %6 = alloca float*, align 8
  %7 = alloca float*, align 8
  %8 = alloca i64, align 8
  %9 = alloca i64, align 8
  store float* %0, float** %5, align 8
  store float* %1, float** %6, align 8
  store float* %2, float** %7, align 8
  store i64 %3, i64* %8, align 8
  store i64 0, i64* %9, align 8
  br label %10

; <label>:10:                                     ; preds = %32, %4
  %11 = load i64, i64* %9, align 8
  %12 = load i64, i64* %8, align 8
  %13 = icmp ult i64 %11, %12
  br i1 %13, label %14, label %35

; <label>:14:                                     ; preds = %10
  %15 = load float*, float** %5, align 8
  %16 = load i64, i64* %9, align 8
  %17 = getelementptr inbounds float, float* %15, i64 %16
  %18 = load float, float* %17, align 4
  %19 = load float*, float** %6, align 8
  %20 = load i64, i64* %9, align 8
  %21 = getelementptr inbounds float, float* %19, i64 %20
  %22 = load float, float* %21, align 4
  %23 = fadd float %18, %22
  %24 = load float*, float** %5, align 8
  %25 = load i64, i64* %9, align 8
  %26 = getelementptr inbounds float, float* %24, i64 %25
  %27 = load float, float* %26, align 4
  %28 = fdiv float %23, %27
  %29 = load float*, float** %7, align 8
  %30 = load i64, i64* %9, align 8
  %31 = getelementptr inbounds float, float* %29, i64 %30
  store float %28, float* %31, align 4
  br label %32

; <label>:32:                                     ; preds = %14
  %33 = load i64, i64* %9, align 8
  %34 = add i64 %33, 1
  store i64 %34, i64* %9, align 8
  br label %10

; <label>:35:                                     ; preds = %10
  ret void
}

; Function Attrs: noinline nounwind optnone uwtable
define void @FuseAddMul(float*, float*, float*, i64) #0 {
  %5 = alloca float*, align 8
  %6 = alloca float*, align 8
  %7 = alloca float*, align 8
  %8 = alloca i64, align 8
  %9 = alloca i64, align 8
  store float* %0, float** %5, align 8
  store float* %1, float** %6, align 8
  store float* %2, float** %7, align 8
  store i64 %3, i64* %8, align 8
  store i64 0, i64* %9, align 8
  br label %10

; <label>:10:                                     ; preds = %32, %4
  %11 = load i64, i64* %9, align 8
  %12 = load i64, i64* %8, align 8
  %13 = icmp ult i64 %11, %12
  br i1 %13, label %14, label %35

; <label>:14:                                     ; preds = %10
  %15 = load float*, float** %5, align 8
  %16 = load i64, i64* %9, align 8
  %17 = getelementptr inbounds float, float* %15, i64 %16
  %18 = load float, float* %17, align 4
  %19 = load float*, float** %6, align 8
  %20 = load i64, i64* %9, align 8
  %21 = getelementptr inbounds float, float* %19, i64 %20
  %22 = load float, float* %21, align 4
  %23 = fmul float %18, %22
  %24 = load float*, float** %7, align 8
  %25 = load i64, i64* %9, align 8
  %26 = getelementptr inbounds float, float* %24, i64 %25
  %27 = load float, float* %26, align 4
  %28 = fadd float %23, %27
  %29 = load float*, float** %7, align 8
  %30 = load i64, i64* %9, align 8
  %31 = getelementptr inbounds float, float* %29, i64 %30
  store float %28, float* %31, align 4
  br label %32

; <label>:32:                                     ; preds = %14
  %33 = load i64, i64* %9, align 8
  %34 = add i64 %33, 1
  store i64 %34, i64* %9, align 8
  br label %10

; <label>:35:                                     ; preds = %10
  ret void
}

; Function Attrs: noinline nounwind optnone uwtable
define i32 @main() #0 {
  %1 = alloca i32, align 4
  %2 = alloca [10 x float], align 16
  %3 = alloca [10 x float], align 16
  %4 = alloca [10 x float], align 16
  %5 = alloca i64, align 8
  store i32 0, i32* %1, align 4
  %6 = getelementptr inbounds [10 x float], [10 x float]* %2, i32 0, i32 0
  %7 = getelementptr inbounds [10 x float], [10 x float]* %3, i32 0, i32 0
  %8 = getelementptr inbounds [10 x float], [10 x float]* %4, i32 0, i32 0
  call void @init(float* %6, float* %7, float* %8, i64 10)
  %9 = getelementptr inbounds [10 x float], [10 x float]* %2, i32 0, i32 0
  %10 = getelementptr inbounds [10 x float], [10 x float]* %3, i32 0, i32 0
  %11 = getelementptr inbounds [10 x float], [10 x float]* %4, i32 0, i32 0
  call void @VectorAdd(float* %9, float* %10, float* %11, i64 10)
  %12 = getelementptr inbounds [10 x float], [10 x float]* %2, i32 0, i32 0
  %13 = getelementptr inbounds [10 x float], [10 x float]* %3, i32 0, i32 0
  %14 = getelementptr inbounds [10 x float], [10 x float]* %4, i32 0, i32 0
  call void @FuseAddMul(float* %12, float* %13, float* %14, i64 10)
  store i64 0, i64* %5, align 8
  br label %15

; <label>:15:                                     ; preds = %24, %0
  %16 = load i64, i64* %5, align 8
  %17 = icmp ult i64 %16, 10
  br i1 %17, label %18, label %27

; <label>:18:                                     ; preds = %15
  %19 = load i64, i64* %5, align 8
  %20 = getelementptr inbounds [10 x float], [10 x float]* %4, i64 0, i64 %19
  %21 = load float, float* %20, align 4
  %22 = fpext float %21 to double
  %23 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([4 x i8], [4 x i8]* @.str, i32 0, i32 0), double %22)
  br label %24

; <label>:24:                                     ; preds = %18
  %25 = load i64, i64* %5, align 8
  %26 = add i64 %25, 1
  store i64 %26, i64* %5, align 8
  br label %15

; <label>:27:                                     ; preds = %15
  %28 = load i32, i32* %1, align 4
  ret i32 %28
}

declare i32 @printf(i8*, ...) #1

attributes #0 = { noinline nounwind optnone uwtable "correctly-rounded-divide-sqrt-fp-math"="false" "disable-tail-calls"="false" "less-precise-fpmad"="false" "no-frame-pointer-elim"="true" "no-frame-pointer-elim-non-leaf" "no-infs-fp-math"="false" "no-jump-tables"="false" "no-nans-fp-math"="false" "no-signed-zeros-fp-math"="false" "no-trapping-math"="false" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+fxsr,+mmx,+sse,+sse2,+x87" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #1 = { "correctly-rounded-divide-sqrt-fp-math"="false" "disable-tail-calls"="false" "less-precise-fpmad"="false" "no-frame-pointer-elim"="true" "no-frame-pointer-elim-non-leaf" "no-infs-fp-math"="false" "no-nans-fp-math"="false" "no-signed-zeros-fp-math"="false" "no-trapping-math"="false" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+fxsr,+mmx,+sse,+sse2,+x87" "unsafe-fp-math"="false" "use-soft-float"="false" }

!llvm.module.flags = !{!0}
!llvm.ident = !{!1}

!0 = !{i32 1, !"wchar_size", i32 4}
!1 = !{!"clang version 6.0.1 (tags/RELEASE_601/final)"}
