#
# Conditional build:
%bcond_without	tests	# do not perform "make test"
#
%define		pdir	Linux
%define		pnam	AIO
Summary:	Linux::AIO - Linux-specific AIO implemented using clone
Summary(pl.UTF-8):	Linux::AIO - linuksowe AIO zaimplementowane przy użyciu clone
Name:		perl-Linux-AIO
Version:	1.9
Release:	4
# same as perl
License:	GPL v1+ or Artistic
Group:		Development/Languages/Perl
Source0:	http://www.cpan.org/modules/by-module/%{pdir}/%{pdir}-%{pnam}-%{version}.tar.gz
# Source0-md5:	8b70ad6bce649c162bbd8733d4405972
URL:		http://search.cpan.org/dist/Linux-AIO/
BuildRequires:	perl-devel >= 1:5.8.0
BuildRequires:	rpm-perlprov >= 4.1-13
ExclusiveArch:	%{ix86} %{x8664} alpha sparc64
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This module implements asynchronous I/O using the means available to
Linux - clone. It does not hook into the POSIX aio_* functions because
Linux does not yet support these in the kernel (and even if, it would
only allow aio_read and write, not open and stat).

Instead, in this module a number of (non-posix) threads are started
that execute your read/writes and signal their completion. You don't
need thread support in your libc or Perl, and the threads created by
this module will not be visible to the pthreads library.

NOTICE: the threads created by this module will automatically be
killed when the thread calling min_parallel exits. Make sure you only
ever call min_parallel from the same thread that loaded this module.

Although the module will work with threads, it is not reentrant, so
use appropriate locking yourself.

%description -l pl.UTF-8
Ten moduł implementuje asynchroniczne I/O przy użyciu środka
dostępnego pod Linuksem - clone. Nie odwołuje się do funkcji POSIX
aio_* ponieważ Linux jeszcze nie obsługuje ich w jądrze (a nawet
gdyby, to pozwoliłby tylko na aio_read i write, a nie open i stat).

Zamiast tego w tym module uruchamiane jest wiele (nie-posiksowych)
wątków wykonujących odczyty/zapisy i sygnalizujących ich zakończenie.
Nie jest wymagana obsługa wątków w libc czy Perlu, a tworzone wątki
nie są widoczne dla biblioteki pthreads.

UWAGA: wątki stworzone przez ten moduł będą automatycznie zabijane po
zakończeniu wątku wywołującego min_parallel. Trzeba upewnić się, że
wywołujemy min_parallel z tego samego wątku, który wczytał ten moduł.

Chociaż ten moduł będzie działał z wątkami, nie jest wielowejściowy
(reentrant), więc odpowiednie blokady trzeba oprogramować samemu.

%prep
%setup -q -n %{pdir}-%{pnam}-%{version}

%build
%{__perl} Makefile.PL \
	INSTALLDIRS=vendor

%{__make} \
	CC="%{__cc}" \
	OPTIMIZE="%{rpmcflags}"

%{?with_tests:%{__make} test}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc Changes
%{perl_vendorarch}/Linux/*.pm
%dir %{perl_vendorarch}/auto/Linux/AIO
%attr(755,root,root) %{perl_vendorarch}/auto/Linux/AIO/AIO.so
%{_mandir}/man3/*
