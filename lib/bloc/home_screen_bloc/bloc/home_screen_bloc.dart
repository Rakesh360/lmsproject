import 'dart:async';

import 'package:bloc/bloc.dart';
import 'package:equatable/equatable.dart';

part 'home_screen_event.dart';
part 'home_screen_state.dart';

class HomeScreenBloc extends Bloc<HomeScreenEvent, HomeScreenState> {
  HomeScreenBloc() : super(HomeScreenInitial());

  @override
  Stream<HomeScreenState> mapEventToState(
    HomeScreenEvent event,
  ) async* {
    if (event is HomeScreenInitialEvent) {
      yield* mapHomeScreenInitialState(event);
    }
  }
}

Stream<HomeScreenState> mapHomeScreenInitialState(
    HomeScreenInitialEvent event) async* {
  yield HomeScreenInitial();
}
